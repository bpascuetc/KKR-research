"""Behavioral tests; synthetic edge cases are not EDGAR evidence."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / '.agents/skills/buffett-edgar/scripts'))
from edgar import TAGS, analyze, checks, numeric_tokens, report, run, unsupported_numbers, year_row


def fixture():
    facts = {'entityName': 'SYNTHETIC TEST ONLY', 'facts': {'us-gaap': {}}}
    for name, tags in TAGS.items():
        entries = []
        for year in range(2022, 2027):
            f = {'form': '10-K', 'end': f'{year}-08-30', 'filed': f'{year}-10-15',
                 'accn': f'{year}-original', 'fy': 2026,
                 'val': (year - 2020) * (20_000_000 if name == 'equity' else 4_000_000)}
            if name != 'equity':
                f['start'] = f'{year - 1}-08-31'
            if name == 'capital_spending':
                f['val'] = 1_000_000
            entries.append(f)
        facts['facts']['us-gaap'][tags[0]] = {'units': {'USD': entries}}
    return facts


class ExtractionTests(unittest.TestCase):
    def test_fiscal_ends_not_filing_fy_and_latest_revision(self):
        f = fixture()
        entries = f['facts']['us-gaap']['NetIncomeLoss']['units']['USD']
        entries += [{**entries[0], 'filed': '2026-11-01', 'accn': 'revision', 'val': 33_000_000},
                    {**entries[0], 'form': '10-Q', 'filed': '2026-11-02', 'val': 999},
                    {**entries[0], 'start': '2022-06-01', 'filed': '2026-11-03', 'val': 888}]
        result = analyze(f, 'FAKE')
        self.assertEqual(len(result['rows']), 5)
        self.assertEqual(result['rows'][0]['fiscal_year_end'], '2022-08-30')
        self.assertEqual(result['rows'][0]['net_income'], 33_000_000)
        self.assertEqual(result['rows'][0]['sources']['net_income']['accn'], 'revision')

    def test_priority_fallback_and_missing_capex(self):
        f = fixture()
        gaap = f['facts']['us-gaap']
        original = gaap.pop(TAGS['capital_spending'][0])
        gaap[TAGS['capital_spending'][1]] = original
        row = year_row(f, '2026-08-30')
        self.assertEqual(row['capital_spending'], 1_000_000)
        self.assertTrue(row['sources']['capital_spending']['tag'].endswith('PaymentsToAcquireProductiveAssets'))
        gaap.pop(TAGS['capital_spending'][1])
        result = analyze(f, 'FAKE')
        self.assertIsNone(result['rows'][0]['owner_earnings'])
        self.assertEqual(list(result['checks'].values())[1:], ['not known', 'not known'])
        self.assertIn('not found', report(result))

    def test_nonpositive_equity_and_missing_middle_year(self):
        f = fixture()
        f['facts']['us-gaap']['StockholdersEquity']['units']['USD'][0]['val'] = 0
        self.assertIsNone(year_row(f, '2022-08-30')['roe_percent'])
        f['facts']['us-gaap']['StockholdersEquity']['units']['USD'][0]['val'] = -1
        self.assertIsNone(year_row(f, '2022-08-30')['roe_percent'])
        result = analyze(f, 'FAKE')
        self.assertEqual(list(result['checks'].values())[0], 'not known')
        result['rows'][2]['owner_earnings'] = None
        self.assertEqual(list(checks(result['rows']).values())[1], 'not known')
        self.assertEqual(list(checks(result['rows']).values())[2], 'pass')

    def test_tag_priority_and_formula(self):
        f = fixture()
        gaap = f['facts']['us-gaap']
        gaap['Revenues'] = {'units': {'USD': [{**gaap[TAGS['revenue'][0]]['units']['USD'][-1], 'filed': '2099-01-01', 'val': 999}]}}
        row = year_row(f, '2026-08-30')
        self.assertEqual(row['revenue'], 24_000_000)
        self.assertEqual(row['owner_earnings'], 23_000_000)
        self.assertAlmostEqual(row['roe_percent'], 20)

    def test_number_audit(self):
        printed = '28.3% 3,501 2022-08-28 15%'
        self.assertEqual(unsupported_numbers('ROE 28.30%; cash 3501; date 2022-08-28', printed), [])
        self.assertEqual(unsupported_numbers('ROE 40.0% and 99.9%', printed), ['40.0%', '99.9%'])
        self.assertEqual(unsupported_numbers('ROE 28.3', printed), ['28.3'])
        self.assertEqual(unsupported_numbers('Cash was 999.', printed), ['999'])


@unittest.skipUnless(importlib.util.find_spec('streamlit'), 'Streamlit requires the course virtual environment')
class AppTests(unittest.TestCase):
    def test_render_probe_and_bank_missing_data(self):
        from streamlit.testing.v1 import AppTest
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'evidence').mkdir()
            (root / 'memos').mkdir()
            cost = fixture()
            bank = fixture()
            del bank['facts']['us-gaap'][TAGS['capital_spending'][0]]
            for ticker, facts in [('COST', cost), ('JPM', bank)]:
                (root / f'evidence/{ticker}_companyfacts.json').write_text(json.dumps(facts))
                result = run(ticker, root / 'evidence', offline=True)
                (root / f'memos/{ticker}_memo.md').write_text('Buffett-inspired synthetic test: watch it.')
            source = (ROOT / 'lab18_app.py').read_text().replace('ROOT = Path(__file__).resolve().parent', f'ROOT = Path({str(root)!r})')
            app = AppTest.from_string(source).run(timeout=30)
            self.assertEqual(list(app.exception), [])
            self.assertEqual(len(app.get('vega_lite_chart')), 1)
            probe = next(b for b in app.button if b.label == 'Insert unsupported ROE probe')
            probe.click().run()
            self.assertTrue(any('40.0%' in item.value for item in app.error))
            app.sidebar.text_input[0].set_value('JPM')
            app.sidebar.button[0].click().run()
            self.assertEqual(list(app.exception), [])
            self.assertTrue(any('Owner earnings not found' in item.value for item in app.warning))
            self.assertIn('not known', str(app.dataframe[1].value))


if __name__ == '__main__':
    unittest.main(verbosity=2)
