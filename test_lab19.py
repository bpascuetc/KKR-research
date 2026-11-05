"""Behavioral checks: unknowns, boundaries, probe, memo binding and actual app."""
from copy import deepcopy
import json
from pathlib import Path
import unittest

import panel
from test_lab18 import fixture


class PanelTests(unittest.TestCase):
    def setUp(self):
        self.result = panel.run('COST', offline=True)

    def test_cost_known_answer_and_probe(self):
        rows = self.result['rows']
        self.assertEqual([round(r['liabilities_to_equity'], 2) for r in rows], [2.11, 1.75, 1.96, 1.64, 1.49])
        self.assertTrue(all(r['research_and_development'] is None for r in rows))
        wood = self.result['panel']['Cathie Wood']
        self.assertEqual(round(wood['metrics']['revenue_growth_percent'], 2), 7.51)
        self.assertEqual(list(wood['checks'].values()), ['fail', 'not known'])
        self.assertEqual(list(self.result['panel']['Buffett']['checks'].values()), ['pass'] * 3)
        self.assertEqual(list(self.result['panel']['Burry']['checks'].values()), ['pass'] * 2)
        changed = panel.cathie_checks(rows, {'growth_threshold_percent': 5, 'rd_threshold_percent': 5})
        self.assertEqual(list(changed['checks'].values()), ['pass', 'not known'])

    def test_missing_inputs_zero_denominators_and_boundaries(self):
        rows = deepcopy(self.result['rows'])
        rows[-1]['revenue'] = None
        self.assertEqual(list(panel.cathie_checks(rows)['checks'].values()), ['not known', 'not known'])
        rows[0]['revenue'] = 0
        self.assertIsNone(panel.cathie_checks(rows)['metrics']['revenue_growth_percent'])
        rows = deepcopy(self.result['rows'])
        rows[-1]['research_and_development'] = rows[-1]['revenue'] * .05
        self.assertEqual(list(panel.cathie_checks(rows)['checks'].values())[1], 'pass')
        for row in rows:
            row['operating_cash_flow'] = row['net_income']
        rows[-1]['liabilities'] = rows[-1]['equity'] * 2
        self.assertEqual(list(panel.burry_checks(rows)['checks'].values()), ['pass', 'pass'])
        rows[-1]['liabilities'] += 1
        self.assertEqual(list(panel.burry_checks(rows)['checks'].values())[1], 'fail')
        rows[2]['operating_cash_flow'] = None
        rows[-1]['equity'] = 0
        self.assertEqual(list(panel.burry_checks(rows)['checks'].values()), ['not known', 'not known'])

    def test_new_tags_annual_instant_latest_filing(self):
        facts = fixture()
        end = '2026-08-30'
        common = {'end': end, 'form': '10-K', 'filed': '2026-10-01', 'accn': 'initial', 'val': 10_000_000}
        facts['facts']['us-gaap']['Liabilities'] = {'units': {'USD': [common,
            {**common, 'filed': '2026-11-01', 'accn': 'revision', 'val': 20_000_000},
            {**common, 'form': '10-Q', 'filed': '2026-11-02', 'val': 999}]}}
        facts['facts']['us-gaap']['ResearchAndDevelopmentExpense'] = {'units': {'USD': [
            {**common, 'start': '2025-08-31', 'val': 2_000_000},
            {**common, 'start': '2026-06-01', 'filed': '2026-11-02', 'val': 888}]}}
        row = panel.analyze(facts, 'FAKE')['rows'][-1]
        self.assertEqual(row['liabilities'], 20_000_000)
        self.assertEqual(row['research_and_development'], 2_000_000)
        self.assertEqual(row['sources']['liabilities']['accn'], 'revision')

    def test_memos_and_stale_binding(self):
        audits = panel.audit(self.result)
        self.assertTrue(all(v['current'] and v['unsupported_numbers'] == [] for v in audits.values()))
        for who in panel.INVESTORS:
            memo = panel.memo_path(self.result, who).read_text()
            self.assertIn('40.0%', panel.edgar.unsupported_numbers(memo + '\nROE 40.0%', panel.report(self.result)))
        changed = deepcopy(self.result)
        changed['rows'][-1]['net_income'] += 1
        for who in panel.INVESTORS:
            self.assertNotEqual(panel.memo_fingerprint(changed, who), panel.memo_fingerprint(self.result, who))


class ActualAppTests(unittest.TestCase):
    def test_actual_nvda_panel_memos_and_cash_failure(self):
        from streamlit.testing.v1 import AppTest
        result = panel.run('NVDA', offline=True)
        audits = panel.audit(result)
        self.assertTrue(all(v['current'] and v['unsupported_numbers'] == [] for v in audits.values()))
        app = AppTest.from_file(str(panel.ROOT / 'app.py')).run(timeout=30)
        app.sidebar.text_input[0].set_value('NVDA')
        app.sidebar.button[0].click().run()
        self.assertEqual(list(app.exception), [])
        table = app.dataframe[0].value
        self.assertEqual(table.Result.tolist(), ['pass', 'pass', 'pass', 'pass', 'pass', 'fail', 'pass'])
        self.assertEqual(len(app.text_area), 3)
        self.assertTrue(all(item.value.strip() for item in app.text_area))
        self.assertFalse(list(app.error))
        self.assertFalse(any('stale' in item.value.lower() for item in app.warning))

    def test_actual_cost_three_memos_each_flagged_and_probe(self):
        from streamlit.testing.v1 import AppTest
        app = AppTest.from_file(str(panel.ROOT / 'app.py')).run(timeout=30)
        self.assertEqual(list(app.exception), [])
        self.assertEqual(len(app.text_area), 3)
        self.assertEqual(len(app.columns), 3)
        self.assertEqual(len(app.dataframe[0].value), 7)
        for who in panel.INVESTORS:
            next(b for b in app.button if b.key == f'probe_COST_{who}').click().run()
            self.assertTrue(any(who in e.value and '40.0%' in e.value for e in app.error))
        app.sidebar.checkbox[0].check().run()
        self.assertEqual(list(app.exception), [])
        table = app.dataframe[0].value
        self.assertEqual(table[table.Investor == 'Cathie Wood'].Result.tolist(), ['pass', 'not known'])
        self.assertFalse(any('stale' in w.value.lower() for w in app.warning))
        app.sidebar.checkbox[0].uncheck().run()
        self.assertEqual(app.dataframe[0].value[app.dataframe[0].value.Investor == 'Cathie Wood'].Result.tolist(), ['fail', 'not known'])
        app.sidebar.text_input[0].set_value('JPM')
        app.sidebar.button[0].click().run()
        self.assertEqual(list(app.exception), [])
        self.assertIn('not known', str(app.dataframe[0].value))
        self.assertTrue(any('Owner earnings not found' in w.value for w in app.warning))
        panel.run('COST', offline=True)


if __name__ == '__main__':
    unittest.main(verbosity=2)
