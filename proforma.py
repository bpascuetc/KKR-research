"""Lab 09: ABG training case; USD millions except per-share values.

Source: instructor assumptions supplied by Bernat on September 22, 2026.
No external data or packages. Run: python3 proforma.py
Run validation: python3 proforma.py --self-test
Demonstrate refusal: python3 proforma.py --break-cash
"""

import argparse
import math
from copy import deepcopy

OPENING = dict(revenue=17999.0, inventory=2135.8, ppe=3070.4,
               other_assets=6371.6, cash=40.4, floor_plan=2027.0,
               debt=3572.0, other_liabilities=2127.5, equity=3891.7,
               revolver=0.0)
ASSUMPTIONS = dict(
    growth=.018, gross_margin=.1705,
    sga_ratios=(.665, .655, .645, .645, .645),
    depreciation_ratio=82.4 / 3070.4, impairment=120.0, capex=250.0,
    tax_rate=.255, inventory_days=2135.8 / (17999.0 - 3071.7) * 365,
    floor_plan_ratio=2027.0 / 2135.8, working_capital_ratio=.008,
    minimum_cash=25.0, revolver_limit=850.0, revolver_rate=.06,
    repayment=150.0, buyback=150.0, floor_plan_rate=.0467,
    debt_rate=.0544, cost_of_equity=.10, terminal_growth=.025,
    shares=17.951349,
)
DISCLAIMER = (
    "I am a student, not a financial professional. This document was prepared "
    "for FIN 43900 (AI Finance Applications, Purdue) as a class learning exercise. "
    "It is not professional investment research or financial advice. I used "
    "OpenAI Codex to help with research, analysis, calculations, and drafting. "
    "Any remaining errors are my own."
)
TOLERANCE = 1e-7


def totals(row):
    assets = sum(row[k] for k in ('cash', 'inventory', 'ppe', 'other_assets'))
    liabilities = sum(row[k] for k in
                      ('floor_plan', 'debt', 'revolver', 'other_liabilities'))
    return assets, liabilities, assets - liabilities - row['equity']


def assert_balanced(rows, assumptions=None):
    """Recompute from actual balances, including after deliberate corruption."""
    a = ASSUMPTIONS if assumptions is None else assumptions
    for row in rows:
        year = row['year']
        if not all(math.isfinite(v) for v in row.values()):
            raise ValueError(f'FY{year}E: nonfinite input; gap undefined')
        gap = totals(row)[2]
        if abs(gap) > TOLERANCE:
            raise ValueError(f'FY{year}E: assets - liabilities - equity gap {gap:+.1f}')
        cash_gap = row['cash'] - a['minimum_cash']
        if cash_gap < -TOLERANCE:
            raise ValueError(f'FY{year}E: minimum cash gap {cash_gap:+.1f}')
        if not -TOLERANCE <= row['revolver'] <= a['revolver_limit'] + TOLERANCE:
            raise ValueError(f"FY{year}E: revolver limit gap "
                             f"{row['revolver'] - a['revolver_limit']:+.1f}")


def project(opening=None, assumptions=None):
    a = ASSUMPTIONS if assumptions is None else assumptions
    prior = dict(OPENING if opening is None else opening)
    if abs(totals(prior)[2]) > TOLERANCE:
        raise ValueError(f'FY2025: opening balance sheet gap {totals(prior)[2]:+.1f}')
    if len(a['sga_ratios']) != 5:
        raise ValueError('Provide five SG&A ratios.')
    rows = []
    for year, sga_ratio in zip(range(2026, 2031), a['sga_ratios']):
        r = dict(year=year)
        r['revenue'] = prior['revenue'] * (1 + a['growth'])
        r['gross_profit'] = r['revenue'] * a['gross_margin']
        r['cost_of_sales'] = r['revenue'] - r['gross_profit']
        r['sga'] = r['gross_profit'] * sga_ratio
        r['depreciation'] = prior['ppe'] * a['depreciation_ratio']
        r['impairment'] = a['impairment']
        r['operating_income'] = r['gross_profit'] - r['sga'] - r['depreciation'] - r['impairment']
        r['interest'] = (prior['floor_plan'] * a['floor_plan_rate']
                         + prior['debt'] * a['debt_rate']
                         + prior['revolver'] * a['revolver_rate'])
        r['pretax'] = r['operating_income'] - r['interest']
        r['tax'] = max(0, r['pretax']) * a['tax_rate']
        r['net_income'] = r['pretax'] - r['tax']
        r['inventory'] = r['cost_of_sales'] * a['inventory_days'] / 365
        r['floor_plan'] = r['inventory'] * a['floor_plan_ratio']
        r['capex'] = a['capex']
        r['ppe'] = prior['ppe'] + r['capex'] - r['depreciation']
        r['change_other_wc'] = a['working_capital_ratio'] * (r['revenue'] - prior['revenue'])
        r['other_assets'] = prior['other_assets'] + r['change_other_wc'] - r['impairment']
        r['repayment'] = a['repayment']
        if not 0 <= r['repayment'] <= prior['debt']:
            raise ValueError(f'FY{year}E: repayment must be between zero and opening debt')
        r['debt'] = prior['debt'] - r['repayment']
        r['other_liabilities'] = prior['other_liabilities']
        r['buyback'] = a['buyback']
        r['equity'] = prior['equity'] + r['net_income'] - r['buyback']
        r['change_inventory'] = r['inventory'] - prior['inventory']
        r['change_floor_plan'] = r['floor_plan'] - prior['floor_plan']
        # Course convention includes the inventory financing change in operating cash flow.
        r['operating_cash_flow'] = (r['net_income'] + r['depreciation'] + r['impairment']
                                    - r['change_inventory'] - r['change_other_wc']
                                    + r['change_floor_plan'])
        r['fcfe'] = r['operating_cash_flow'] - r['capex'] - r['repayment']
        r['opening_cash'] = prior['cash']
        cash_before_revolver = prior['cash'] + r['fcfe'] - r['buyback']
        if cash_before_revolver < a['minimum_cash']:
            r['change_revolver'] = min(a['minimum_cash'] - cash_before_revolver,
                                       a['revolver_limit'] - prior['revolver'])
        else:
            r['change_revolver'] = -min(prior['revolver'], cash_before_revolver - a['minimum_cash'])
        r['revolver'] = prior['revolver'] + r['change_revolver']
        r['cash'] = cash_before_revolver + r['change_revolver']
        r['investing_cash_flow'] = -r['capex']
        r['financing_cash_flow'] = -r['repayment'] - r['buyback'] + r['change_revolver']
        r['change_cash'] = r['operating_cash_flow'] + r['investing_cash_flow'] + r['financing_cash_flow']
        rows.append(r)
        prior = r
    return rows


def value_equity(rows, assumptions=None):
    a = ASSUMPTIONS if assumptions is None else assumptions
    assert_balanced(rows, a)  # Mandatory gate before any valuation.
    k, g = a['cost_of_equity'], a['terminal_growth']
    if not (-1 < g < k) or a['shares'] <= 0:
        raise ValueError('Require cost of equity > terminal growth > -100% and positive shares.')
    explicit_pv = sum(r['fcfe'] / (1 + k) ** t for t, r in enumerate(rows, 1))
    terminal = (rows[-1]['fcfe'] + rows[-1]['repayment']) * (1 + g) / (k - g)
    terminal_pv = terminal / (1 + k) ** len(rows)
    equity = explicit_pv + terminal_pv
    return dict(explicit_pv=explicit_pv, terminal_pv=terminal_pv, equity=equity,
                terminal_share=terminal_pv / equity, price=equity / a['shares'])


def print_table(title, rows, fields):
    print('\n' + title)
    print(f"{'USD millions':<34}" + ''.join(f"{'FY' + str(r['year']) + 'E':>13}" for r in rows))
    for label, key in fields:
        values = [key(r) if callable(key) else r[key] for r in rows]
        print(f'{label:<34}' + ''.join(f'{0 if abs(v) < TOLERANCE else v:13,.1f}' for v in values))


def self_test():
    rows = project()
    for index, expected in ((0, (18323.0, 844.2, 413.6, 211.4, 101.8)),
                            (4, (19678.3, 971.4, 527.5, 342.3, 719.8))):
        for key, number in zip(('revenue', 'operating_income', 'net_income', 'fcfe', 'cash'), expected):
            assert f'{rows[index][key]:.1f}' == f'{number:.1f}', (index, key)
    assert f"{value_equity(rows)['price']:.2f}" == '291.75'
    broken = deepcopy(rows)
    broken[0]['cash'] = OPENING['cash']
    try:
        value_equity(broken)
    except ValueError as exc:
        assert 'FY2026E' in str(exc) and '-61.4' in str(exc)
        print('PASS deliberate cash break:', exc)
    else:
        raise AssertionError('Broken cash was accepted')
    # Exercise draw, next-year interest, repayment priority, and exhausted capacity.
    stress = dict(ASSUMPTIONS, buyback=260.0)
    drawn = project(assumptions=stress)
    assert_balanced(drawn, stress)
    assert drawn[0]['revolver'] > 0 and abs(drawn[0]['cash'] - 25) < TOLERANCE
    assert drawn[-1]['revolver'] < drawn[0]['revolver']
    expected_interest = sum(drawn[0][key] * stress[rate] for key, rate in
                            (('floor_plan', 'floor_plan_rate'), ('debt', 'debt_rate'), ('revolver', 'revolver_rate')))
    assert abs(drawn[1]['interest'] - expected_interest) < TOLERANCE
    limited = dict(stress, revolver_limit=1.0)
    try:
        value_equity(project(assumptions=limited), limited)
    except ValueError as exc:
        assert 'minimum cash gap' in str(exc)
    else:
        raise AssertionError('Insufficient revolver capacity was accepted')
    print('PASS all published benchmarks, five balance checks, and revolver scenarios')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--break-cash', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    rows = project()
    if args.break_cash:
        rows[0]['cash'] = OPENING['cash']
    print('ABG — Lab 09 instructor training assumptions, September 22, 2026')
    print_table('INCOME STATEMENT', rows, [(k.replace('_', ' ').title(), k) for k in
                ('revenue', 'cost_of_sales', 'gross_profit', 'sga', 'depreciation', 'impairment',
                 'operating_income', 'interest', 'pretax', 'tax', 'net_income')])
    print_table('BALANCE SHEET', rows, [(k.replace('_', ' ').title(), k) for k in
                ('cash', 'inventory', 'ppe', 'other_assets')] + [('Total assets', lambda r: totals(r)[0])]
                + [(k.replace('_', ' ').title(), k) for k in ('floor_plan', 'debt', 'revolver', 'other_liabilities')]
                + [('Total liabilities', lambda r: totals(r)[1]), ('Equity', 'equity')])
    print_table('CASH FLOW (floor-plan change included in operating)', rows,
                [(k.replace('_', ' ').title(), k) for k in
                 ('net_income', 'depreciation', 'impairment')]
                + [('Less inventory change', lambda r: -r['change_inventory']),
                   ('Less other WC change', lambda r: -r['change_other_wc'])]
                + [(k.replace('_', ' ').title(), k) for k in
                   ('change_floor_plan', 'operating_cash_flow', 'investing_cash_flow')]
                + [('Less debt repayment', lambda r: -r['repayment']), ('FCFE before revolver', 'fcfe'),
                   ('Less buyback', lambda r: -r['buyback'])]
                + [(k.replace('_', ' ').title(), k) for k in
                   ('change_revolver', 'financing_cash_flow', 'change_cash', 'opening_cash', 'cash')])
    print_table('CHECKS (cash headroom must be nonnegative)', rows,
                [('Assets - liabilities - equity', lambda r: totals(r)[2]),
                 ('Cash minus minimum', lambda r: r['cash'] - ASSUMPTIONS['minimum_cash'])])
    v = value_equity(rows)
    print('\nAll five years: balance PASS; minimum cash PASS; revolver limit PASS')
    print(f"PV of five FCFE: ${v['explicit_pv']:,.2f} million")
    print(f"PV of terminal value: ${v['terminal_pv']:,.2f} million")
    print(f"Equity value: ${v['equity']:,.2f} million")
    print(f"Share of value after 2030: {v['terminal_share']:.2%}")
    print(f"Value per share: ${v['price']:.2f}")
    print('\n' + DISCLAIMER)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, AssertionError) as error:
        raise SystemExit(f'MODEL REFUSED: {error}') from error

# I am a student, not a financial professional. This document was prepared for
# FIN 43900 (AI Finance Applications, Purdue) as a class learning exercise.
# It is not professional investment research or financial advice. I used OpenAI
# Codex to help with research, analysis, calculations, and drafting.
# Any remaining errors are my own.
