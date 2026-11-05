"""Independent classroom comparison oracle. Extraction never reads these anchors."""
import json
from pathlib import Path
import panel


def verify():
    result = panel.run('COST', offline=True)
    checks = {
        'fiscal_ends_match': [r['fiscal_year_end'] for r in result['rows']] == ['2022-08-28', '2023-09-03', '2024-09-01', '2025-08-31', '2026-08-30'],
        'liabilities_ratios_match': [round(r['liabilities_to_equity'], 2) for r in result['rows']] == [2.11, 1.75, 1.96, 1.64, 1.49],
        'rd_missing_all_years': all(r['research_and_development'] is None for r in result['rows']),
        'growth_matches': round(result['panel']['Cathie Wood']['metrics']['revenue_growth_percent'], 2) == 7.51,
        'buffett_checks_match': list(result['panel']['Buffett']['checks'].values()) == ['pass'] * 3,
        'wood_checks_match': list(result['panel']['Cathie Wood']['checks'].values()) == ['fail', 'not known'],
        'burry_checks_match': list(result['panel']['Burry']['checks'].values()) == ['pass'] * 2,
    }
    saved_probe = json.loads((panel.ROOT / 'evidence/COST_probe_5_results.json').read_text())
    checks['skill_config_probe_matches'] = list(saved_probe['panel']['Cathie Wood']['checks'].values()) == ['pass', 'not known']
    checks['probe_facts_unchanged'] = saved_probe['rows'] == result['rows']
    checks['kept_threshold_restored'] = panel.configuration()['growth_threshold_percent'] == 15
    checks['memos_current_and_supported'] = all(v['current'] and v['unsupported_numbers'] == [] for v in panel.audit(result).values())
    evidence = {'checks': checks, 'all_pass': all(checks.values()), 'memo_audits': panel.audit(result),
                'raw_sha256': result['raw_sha256'], 'source': 'Archived direct SEC download retained from Lab18; no new download claimed.'}
    (panel.ROOT / 'evidence/LAB19_VERIFICATION.json').write_text(json.dumps(evidence, indent=2) + '\n')
    print(json.dumps(evidence, indent=2))
    return evidence['all_pass']


if __name__ == '__main__':
    raise SystemExit(0 if verify() else 1)
