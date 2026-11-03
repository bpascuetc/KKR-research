"""Compare computed SEC outputs with instructor anchors; never feed anchors to extraction."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / '.agents/skills/buffett-edgar/scripts'))
from edgar import unsupported_numbers

ANCHORS = [
    ['2022-08-28', 226954, 5844, 7392, 3891, 20642, 28.3, 3501],
    ['2023-09-03', 242290, 6292, 11068, 4323, 25058, 25.1, 6745],
    ['2024-09-01', 254453, 7367, 11339, 4710, 23622, 31.2, 6629],
    ['2025-08-31', 275235, 8099, 13335, 5498, 29164, 27.8, 7837],
    ['2026-08-30', 303154, 9226, 15817, 6435, 35803, 25.8, 9382],
]
FIELDS = ['revenue', 'net_income', 'operating_cash_flow', 'capital_spending', 'equity', 'roe_percent', 'owner_earnings']


def verify():
    cost = json.loads((ROOT / 'evidence/COST_results.json').read_text())
    jpm = json.loads((ROOT / 'evidence/JPM_results.json').read_text())
    differences = []
    actual = {row['fiscal_year_end']: row for row in cost['rows']}
    for end, *expected in ANCHORS:
        if end not in actual:
            differences.append({'period': end, 'issue': 'missing fiscal year'})
            continue
        for field, target in zip(FIELDS, expected):
            value = actual[end][field]
            scaled = None if value is None else (round(value, 1) if field == 'roe_percent' else value / 1e6)
            if scaled != target:
                differences.append({'period': end, 'field': field, 'expected': target, 'actual': scaled})
    check = {
        'COST_anchor_matches': not differences,
        'COST_differences': differences,
        'COST_checks_all_pass': list(cost['checks'].values()) == ['pass'] * 3,
        'JPM_capex_missing_all_years': all(row['capital_spending'] is None for row in jpm['rows']),
        'JPM_owner_earnings_missing_all_years': all(row['owner_earnings'] is None for row in jpm['rows']),
        'JPM_owner_checks_unknown': list(jpm['checks'].values())[1:] == ['not known', 'not known'],
    }
    for ticker in ('COST', 'JPM'):
        printed = (ROOT / f'evidence/{ticker}_printed.md').read_text()
        path = ROOT / f'memos/{ticker}_memo.md'
        check[f'{ticker}_memo_unsupported_numbers'] = unsupported_numbers(path.read_text(), printed) if path.exists() else 'memo missing'
    printed = (ROOT / 'evidence/COST_printed.md').read_text()
    check['injected_40_percent_flagged'] = '40.0%' in unsupported_numbers('ROE was 40.0%.', printed)
    (ROOT / 'evidence/verification.json').write_text(json.dumps(check, indent=2) + '\n')
    print(json.dumps(check, indent=2))
    return check


if __name__ == '__main__':
    verify()
