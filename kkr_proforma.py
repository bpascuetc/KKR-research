"""Lab 10: simplified KKR consolidated scenario, USD millions.

Standard library only. Read Lab10_KKR.md before interpreting the value.
GAAP opening balances; projected cash realization, ownership allocations and
insurance remittances are classroom judgments, not an actuarial model.
"""
from copy import deepcopy
from datetime import date
import argparse
import csv
import json
import math
from pathlib import Path

DISCLAIMER = ('I am a student, not a financial professional. This document was prepared '
              'for FIN 43900 (AI Finance Applications, Purdue) as a class learning exercise. '
              'It is not professional investment research or financial advice. I used OpenAI '
              'Codex to help with research, analysis, calculations, and drafting. '
              'Any remaining errors are my own.')
TOL = 1e-6  # USD millions, i.e. one dollar
VALUATION_DATE = date(2026, 9, 24)
MARKET_PRICE = 95.64
MARKET_TIMESTAMP = 'September 24, 2026, 4:00 p.m. EDT (provider header; see report for discrepancy)'

# FY2025 10-K pp.159-160, 163-164, 169-170, 250. Divide $thousands by 1,000.
# Split corporate cash using p.126's reconciliation; exclude short-term investments.
OPENING = dict(
    year=2025, corporate_cash=4562.361, other_cash=12329.786,
    restricted_cash=259.643, am_investments=127948.305,
    insurance_investments=192009.748, ppe=975.498,
    insurance_intangibles=5905.228,
    other_assets=66153.503,  # sum of separately reported remaining assets, see report
    am_debt=49117.744, insurance_debt=3820.407, revolver=0.,
    policy_liabilities=205558.727, other_liabilities=70015.283,
    kkr_equity=30902.561, nci_equity=48019.108, redeemable_nci=2710.242,
    fees=4064.273, capital_income=3771.235,
    occupancy=135.941, ga_cash=1479.796-81.4,
    premiums=3397.186, policy_fees=1350.814, insurance_other_income=256.763,
    cash_policy_claims=10731.153-4990.209,
    policy_amortization=309.319, insurance_expenses=594.724+756.019,
    policy_acquisition_spending=1062.606,
)

# All forecast extensions of historical ratios remain JUDGMENTS; sources in report.
ASSUMPTIONS = dict(
    fee_growth=.10, capital_income_growth=.05, insurance_growth=.05,
    overhead_growth=.05, compensation_ratio=4710.394/7835.508,
    depreciation_rate=81.4/902.896, capex=160.765, capex_growth=.05,
    am_gain_yield=.03, gain_cash_fraction=.25, carry_cash_fraction=.60,
    am_dividend_yield=1440.790/((106453.051+127948.305)/2),
    am_interest_yield=3181.871/((106453.051+127948.305)/2),
    insurance_yield=7665.106/((170144.744+192009.748)/2),
    am_debt_rate=2776.946/((45933.920+49117.744)/2),
    insurance_debt_rate=294.969/((3713.336+3820.407)/2),
    policy_credit_rate=4990.209/185205.366,
    deposit_rate=(28507.218-21483.334)/185205.366,
    tax_rate=.25, incremental_wc=.02, common_retention=.20,
    nci_fraction=3619.846/6145.412, redeemable_fraction=155.103/6145.412,
    minimum_cash=1000., revolver_limit=1000., revolver_rate=.06,
    shares=891.451844+20.8, annual_dividend_per_share=.78,
    cost_of_equity=.04+1.7930*.05, terminal_growth=.03,
)

ASSET_KEYS = ('corporate_cash', 'other_cash', 'restricted_cash', 'am_investments',
              'insurance_investments', 'ppe', 'insurance_intangibles', 'other_assets')
LIABILITY_KEYS = ('am_debt', 'insurance_debt', 'revolver', 'policy_liabilities', 'other_liabilities')


def totals(row):
    assets = sum(row[k] for k in ASSET_KEYS)
    liabilities = sum(row[k] for k in LIABILITY_KEYS)
    equity = row['kkr_equity'] + row['nci_equity']
    return assets, liabilities, equity, assets-liabilities-equity-row['redeemable_nci']


def validate_inputs(a, opening):
    if not all(math.isfinite(v) for v in [*a.values(), *opening.values()]):
        raise ValueError('Inputs must be finite')
    for key in ('gain_cash_fraction', 'carry_cash_fraction', 'tax_rate',
                'common_retention', 'nci_fraction', 'redeemable_fraction'):
        if not 0 <= a[key] <= 1:
            raise ValueError(f'{key} must be between zero and one')
    if a['nci_fraction']+a['redeemable_fraction'] >= 1:
        raise ValueError('Outside ownership fractions must sum to less than one')
    if not -1 < a['terminal_growth'] < a['cost_of_equity']:
        raise ValueError('Require cost of equity > terminal growth > -100%')
    if a['shares'] <= 0 or min(a['minimum_cash'], a['revolver_limit'], a['capex']) < 0:
        raise ValueError('Invalid shares, cash floor, revolver limit or capex')
    if any(a[k] <= -1 for k in ('fee_growth', 'capital_income_growth', 'insurance_growth',
                               'overhead_growth', 'capex_growth')):
        raise ValueError('Growth must exceed -100%')
    if abs(totals(opening)[3]) > TOL:
        raise ValueError(f"FY2025 opening balance gap {totals(opening)[3]:+.6f}")


def project(assumptions=None, opening=None):
    a = dict(ASSUMPTIONS if assumptions is None else assumptions)
    prior = dict(OPENING if opening is None else opening)
    validate_inputs(a, prior)
    rows = []
    for t, year in enumerate(range(2026, 2031)):
        r = dict(prior, year=year)
        r['fees'] = prior['fees']*(1+a['fee_growth'])
        r['capital_income'] = prior['capital_income']*(1+a['capital_income_growth'])
        r['am_revenue'] = r['fees']+r['capital_income']
        r['compensation'] = a['compensation_ratio']*r['am_revenue']
        r['occupancy'] = prior['occupancy']*(1+a['overhead_growth'])
        r['ga_cash'] = prior['ga_cash']*(1+a['overhead_growth'])
        r['depreciation'] = prior['ppe']*a['depreciation_rate']
        r['am_expenses'] = r['compensation']+r['occupancy']+r['ga_cash']+r['depreciation']
        for key in ('premiums', 'policy_fees', 'insurance_other_income', 'cash_policy_claims',
                    'policy_amortization', 'insurance_expenses', 'policy_acquisition_spending'):
            r[key] = prior[key]*(1+a['insurance_growth'])
        r['insurance_investment_income'] = prior['insurance_investments']*a['insurance_yield']
        # No separate forecast of insurance fair-value gains/losses or OCI.
        r['insurance_revenue'] = sum(r[k] for k in
            ('premiums', 'policy_fees', 'insurance_other_income', 'insurance_investment_income'))
        r['policy_credit'] = prior['policy_liabilities']*a['policy_credit_rate']
        r['net_deposits'] = prior['policy_liabilities']*a['deposit_rate']
        r['insurance_interest'] = prior['insurance_debt']*a['insurance_debt_rate']
        r['insurance_total_expenses'] = sum(r[k] for k in
            ('cash_policy_claims', 'policy_credit', 'policy_amortization',
             'insurance_expenses', 'insurance_interest'))
        r['revenue'] = r['am_revenue']+r['insurance_revenue']
        r['expenses'] = r['am_expenses']+r['insurance_total_expenses']
        r['investment_gains'] = prior['am_investments']*a['am_gain_yield']
        r['dividend_income'] = prior['am_investments']*a['am_dividend_yield']
        r['interest_income'] = prior['am_investments']*a['am_interest_yield']
        r['am_interest'] = prior['am_debt']*a['am_debt_rate']
        r['revolver_interest'] = prior['revolver']*a['revolver_rate']
        r['investment_income_net'] = (r['investment_gains']+r['dividend_income']+
            r['interest_income']-r['am_interest']-r['revolver_interest'])
        r['pretax'] = r['revenue']-r['expenses']+r['investment_income_net']
        r['tax'] = max(0., r['pretax'])*a['tax_rate']
        r['net_income'] = r['pretax']-r['tax']
        # Consolidated income's ownership allocation is a scenario, not legal ownership %.
        r['nci_income'] = r['net_income']*a['nci_fraction']
        r['redeemable_income'] = r['net_income']*a['redeemable_fraction']
        r['kkr_income'] = r['net_income']-r['nci_income']-r['redeemable_income']
        r['unrealized_gains'] = r['investment_gains']*(1-a['gain_cash_fraction'])
        r['uncollected_carry'] = r['capital_income']*(1-a['carry_cash_fraction'])
        r['unpaid_carry_comp'] = r['uncollected_carry']*a['compensation_ratio']
        r['change_wc'] = a['incremental_wc']*(r['fees']-prior['fees'])
        r['capex'] = a['capex']*(1+a['capex_growth'])**t
        # DAC spending remains operating, consistent with the filing.
        r['operating_cash_flow'] = (r['net_income']+r['depreciation']+
            r['policy_amortization']+r['policy_credit']-r['unrealized_gains']-
            r['uncollected_carry']+r['unpaid_carry_comp']-r['change_wc']-
            r['policy_acquisition_spending'])
        # Credited interest must be invested to back policy liabilities; it is not FCFE.
        r['cash_before_owners'] = r['operating_cash_flow']-r['capex']-r['policy_credit']
        r['nci_distribution'] = max(0., r['cash_before_owners'])*a['nci_fraction']
        r['redeemable_distribution'] = max(0., r['cash_before_owners'])*a['redeemable_fraction']
        r['common_cash_before_retention'] = (r['cash_before_owners']-
            r['nci_distribution']-r['redeemable_distribution'])
        r['retained_insurance_capital'] = max(0., r['common_cash_before_retention'])*a['common_retention']
        r['fcfe'] = r['common_cash_before_retention']-r['retained_insurance_capital']
        r['insurance_investment_purchases'] = (r['net_deposits']+r['policy_credit']+
                                              r['retained_insurance_capital'])
        r['investing_cash_flow'] = -r['capex']-r['insurance_investment_purchases']
        r['common_dividend'] = a['shares']*a['annual_dividend_per_share']
        # Ring-fenced cash cannot pay corporate dividends or meet the corporate floor.
        before = prior['corporate_cash']+r['fcfe']-r['common_dividend']
        if before < a['minimum_cash']:
            r['change_revolver'] = min(a['minimum_cash']-before,
                                       a['revolver_limit']-prior['revolver'])
        else:
            r['change_revolver'] = -min(prior['revolver'], before-a['minimum_cash'])
        r['revolver'] = prior['revolver']+r['change_revolver']
        r['corporate_cash'] = before+r['change_revolver']
        r['financing_cash_flow'] = (r['net_deposits']+r['change_revolver']-
            r['nci_distribution']-r['redeemable_distribution']-r['common_dividend'])
        r['change_cash'] = r['operating_cash_flow']+r['investing_cash_flow']+r['financing_cash_flow']
        r['am_investments'] = prior['am_investments']+r['unrealized_gains']+r['uncollected_carry']
        r['insurance_investments'] = prior['insurance_investments']+r['insurance_investment_purchases']
        r['ppe'] = prior['ppe']+r['capex']-r['depreciation']
        r['insurance_intangibles'] = (prior['insurance_intangibles']+
            r['policy_acquisition_spending']-r['policy_amortization'])
        r['other_assets'] = prior['other_assets']+r['change_wc']
        r['policy_liabilities'] = prior['policy_liabilities']+r['net_deposits']+r['policy_credit']
        r['other_liabilities'] = prior['other_liabilities']+r['unpaid_carry_comp']
        r['kkr_equity'] = prior['kkr_equity']+r['kkr_income']-r['common_dividend']
        r['nci_equity'] = prior['nci_equity']+r['nci_income']-r['nci_distribution']
        r['redeemable_nci'] = prior['redeemable_nci']+r['redeemable_income']-r['redeemable_distribution']
        rows.append(r)
        prior = r
    return rows


def check_rows(rows, assumptions=None, opening=None):
    a = ASSUMPTIONS if assumptions is None else assumptions
    prior = OPENING if opening is None else opening
    validate_inputs(a, prior)
    if len(rows) != 5:
        raise ValueError('Require five projected years')
    for expected_year, r in zip(range(2026, 2031), rows):
        year = r['year']
        if year != expected_year or not all(math.isfinite(x) for x in r.values()):
            raise ValueError(f'FY{year}: invalid year or nonfinite values')
        checks = {
            'assets - liabilities - equity - redeemable NCI': totals(r)[3],
            'cash-flow link': r['corporate_cash']-prior['corporate_cash']-
                r['operating_cash_flow']-r['investing_cash_flow']-r['financing_cash_flow'],
            'KKR equity rollforward': r['kkr_equity']-prior['kkr_equity']-r['kkr_income']+r['common_dividend'],
            'NCI rollforward': r['nci_equity']-prior['nci_equity']-r['nci_income']+r['nci_distribution'],
            'redeemable NCI rollforward': r['redeemable_nci']-prior['redeemable_nci']-r['redeemable_income']+r['redeemable_distribution'],
            'income attribution': r['net_income']-r['kkr_income']-r['nci_income']-r['redeemable_income'],
            'PP&E rollforward': r['ppe']-prior['ppe']-r['capex']+r['depreciation'],
            'insurance asset backing': r['insurance_investments']-prior['insurance_investments']-
                (r['policy_liabilities']-prior['policy_liabilities'])-r['retained_insurance_capital'],
            'FCFE reconciliation': r['fcfe']-(r['operating_cash_flow']+r['investing_cash_flow']+
                r['net_deposits']-r['nci_distribution']-r['redeemable_distribution']),
            'ring-fenced cash': r['other_cash']-prior['other_cash'],
        }
        for label, gap in checks.items():
            if abs(gap) > TOL:
                raise ValueError(f'FY{year} {label} gap {gap:+.6f}')
        if r['corporate_cash'] < a['minimum_cash']-TOL:
            raise ValueError(f"FY{year} corporate cash below floor by {a['minimum_cash']-r['corporate_cash']:.6f}")
        if not -TOL <= r['revolver'] <= a['revolver_limit']+TOL:
            raise ValueError(f'FY{year} revolver exceeds permitted capacity')
        if min(r[k] for k in ASSET_KEYS+LIABILITY_KEYS) < -TOL:
            raise ValueError(f'FY{year} negative asset or liability balance')
        prior = r


def value_equity(rows, assumptions=None, opening=None):
    a = ASSUMPTIONS if assumptions is None else assumptions
    check_rows(rows, a, opening)  # Never value unchecked statements.
    # Remaining FY2026 only: uniform-accrual approximation, not an actual YTD bridge.
    stub = (date(2026, 12, 31)-VALUATION_DATE).days/365
    k, g = a['cost_of_equity'], a['terminal_growth']
    signed_pv = sum(r['fcfe']*(stub if i == 0 else 1)/(1+k)**(stub+i)
                    for i, r in enumerate(rows))
    positive_pv = sum(max(0., r['fcfe'])*(stub if i == 0 else 1)/(1+k)**(stub+i)
                      for i, r in enumerate(rows))
    terminal = rows[-1]['fcfe']*(1+g)/(k-g) if rows[-1]['fcfe'] > 0 else 0.
    terminal_pv = terminal/(1+k)**(stub+4)
    # Approximate valuation-date corporate cash using uniform FY2026 cash movement.
    # Exclude the operating floor and offset revolver borrowings. Fund/insurance cash
    # is never added. Other debt is already serviced in FCFE; no second subtraction.
    start = OPENING if opening is None else opening
    cash_at_date = start['corporate_cash']+(1-stub)*(rows[0]['corporate_cash']-start['corporate_cash'])
    revolver_at_date = start['revolver']+(1-stub)*(rows[0]['revolver']-start['revolver'])
    excess_cash = max(0., cash_at_date-a['minimum_cash'])-revolver_at_date
    equity = positive_pv+terminal_pv+excess_cash
    return dict(equity=equity, price=equity/a['shares'], explicit_pv=positive_pv,
                terminal_pv=terminal_pv, terminal_share=terminal_pv/equity if equity else 0.,
                signed_equity=signed_pv+terminal_pv+excess_cash,
                signed_price=(signed_pv+terminal_pv+excess_cash)/a['shares'],
                excess_cash=excess_cash, estimated_corporate_cash_at_date=cash_at_date,
                stub=stub, negative_years=[r['year'] for r in rows if r['fcfe'] < 0],
                terminal_supported=rows[-1]['fcfe'] > 0)


TABLES = {
    'Income statement': [('Asset-management fees and other','fees'),
        ('Capital allocation income','capital_income'), ('AM revenue','am_revenue'),
        ('Insurance revenue','insurance_revenue'), ('Total revenue','revenue'),
        ('AM compensation','compensation'), ('AM occupancy','occupancy'),
        ('AM G&A excluding fixed-asset D&A','ga_cash'), ('Fixed-asset depreciation','depreciation'),
        ('Insurance cash policy claims proxy','cash_policy_claims'), ('Policy interest credited','policy_credit'),
        ('Policy acquisition amortization','policy_amortization'), ('Insurance debt interest','insurance_interest'),
        ('Insurance other expenses','insurance_expenses'), ('Total expenses','expenses'),
        ('AM investment gains','investment_gains'), ('AM dividend income','dividend_income'),
        ('AM interest income','interest_income'), ('AM debt interest','am_interest'),
        ('Corporate revolver interest','revolver_interest'), ('AM investment income, net','investment_income_net'),
        ('Pretax income','pretax'), ('Tax expense','tax'), ('Consolidated net income','net_income'),
        ('NCI net income','nci_income'), ('Redeemable NCI net income','redeemable_income'),
        ('KKR as-converted common net income','kkr_income')],
    'Balance sheet': [(k.replace('_',' ').title(), k) for k in ASSET_KEYS+LIABILITY_KEYS]+
        [('KKR equity','kkr_equity'), ('NCI equity','nci_equity'), ('Redeemable NCI (mezzanine)','redeemable_nci')],
    'Cash flow and common FCFE': [('Consolidated net income','net_income'),
        ('Add fixed-asset depreciation','depreciation'), ('Add policy amortization','policy_amortization'),
        ('Add interest credited','policy_credit'), ('Unrealized gains (deduct)','unrealized_gains'),
        ('Uncollected carry (deduct)','uncollected_carry'), ('Add unpaid carry compensation','unpaid_carry_comp'),
        ('Working capital increase (deduct)','change_wc'), ('Policy acquisition spending (deduct)','policy_acquisition_spending'),
        ('Operating cash flow','operating_cash_flow'), ('Capex (outflow)','capex'),
        ('Insurance investment purchases (outflow)','insurance_investment_purchases'),
        ('Investing cash flow','investing_cash_flow'), ('Net policyholder deposits','net_deposits'),
        ('NCI distributions (outflow)','nci_distribution'), ('Redeemable distributions (outflow)','redeemable_distribution'),
        ('Common dividend (outflow)','common_dividend'), ('Net revolver draw / repayment','change_revolver'),
        ('Financing cash flow','financing_cash_flow'), ('Change in cash','change_cash'),
        ('Common cash before capital retention','common_cash_before_retention'),
        ('Retained insurance capital (deduct)','retained_insurance_capital'), ('Common FCFE before revolver','fcfe')],
}


def markdown_tables(rows):
    blocks = []
    for title, fields in TABLES.items():
        lines = [f'## {title}', '', '| USD millions | '+' | '.join(f"FY{r['year']}E" for r in rows)+' |',
                 '|---|'+'---:|'*len(rows)]
        for label, key in fields:
            lines.append('| '+label+' | '+' | '.join(f'{r[key]:,.3f}' for r in rows)+' |')
        if title == 'Balance sheet':
            for label, idx in [('Total assets',0), ('Total liabilities',1), ('Total equity excluding redeemable NCI',2),
                               ('Assets - liabilities - equity - redeemable NCI',3)]:
                lines.append('| '+label+' | '+' | '.join(f'{0 if abs(totals(r)[idx])<TOL else totals(r)[idx]:,.3f}' for r in rows)+' |')
        blocks.append('\n'.join(lines))
    return '\n\n'.join(blocks)


def self_test():
    rows = project()
    result = value_equity(rows)
    assert abs(totals(OPENING)[0]-410144.072) < TOL
    assert abs(totals(OPENING)[1]-328512.161) < TOL
    # Break the actual balance; a printed/stored check cannot conceal this.
    broken = deepcopy(rows)
    broken[0]['corporate_cash'] -= 100
    try:
        value_equity(broken)
    except ValueError as exc:
        assert 'FY2026' in str(exc) and '-100.000000' in str(exc)
        print('PASS deliberate break:', exc)
    else:
        raise AssertionError('Corrupt statements were valued')
    # Coordinated balance-sheet edit must still fail the independent cash-flow link.
    broken = deepcopy(rows)
    broken[0]['corporate_cash'] += 100
    broken[0]['kkr_equity'] += 100
    try:
        value_equity(broken)
    except ValueError as exc:
        assert 'cash-flow link' in str(exc)
    else:
        raise AssertionError('Balanced but unlinked edits accepted')
    # A one-off low opening cash buffer draws the revolver, then repays it.
    opening = dict(OPENING, corporate_cash=1000., other_assets=OPENING['other_assets']+3562.361)
    stressed = dict(ASSUMPTIONS, annual_dividend_per_share=rows[0]['fcfe']/ASSUMPTIONS['shares']+.20)
    drawn = project(stressed, opening)
    # Exercise borrowing using a deliberately tighter first-year cash budget.
    if not any(r['revolver'] > 0 for r in drawn):
        stressed['annual_dividend_per_share'] = rows[0]['fcfe']/ASSUMPTIONS['shares']+.20
        drawn = project(stressed, opening)
    check_rows(drawn, stressed, opening)
    assert drawn[0]['revolver'] > 0
    assert abs(drawn[1]['revolver_interest']-drawn[0]['revolver']*stressed['revolver_rate']) < TOL
    limited = dict(stressed, revolver_limit=0.)
    try:
        value_equity(project(limited, opening), limited, opening)
    except ValueError as exc:
        assert 'cash below floor' in str(exc)
    else:
        raise AssertionError('Unfunded cash shortage accepted')
    # Cash realization changes cash value, while all accounting links still balance.
    lower_cash = dict(ASSUMPTIONS, carry_cash_fraction=.40)
    v_low = value_equity(project(lower_cash), lower_cash)
    assert v_low['price'] < result['price']
    # Deposit funding is not immediate common-share cash generation.
    more_deposits = dict(ASSUMPTIONS, deposit_rate=ASSUMPTIONS['deposit_rate']*2)
    funded = project(more_deposits)
    check_rows(funded, more_deposits)
    assert abs(funded[0]['fcfe']-rows[0]['fcfe']) < TOL
    assert funded[0]['insurance_investments'] > rows[0]['insurance_investments']
    # Negative cash flow must remain visible; terminal capitalization is withheld.
    negative = dict(ASSUMPTIONS, capex=10000., revolver_limit=100000.)
    neg = value_equity(project(negative), negative)
    assert neg['negative_years'] and not neg['terminal_supported']
    assert neg['signed_equity'] < neg['equity']
    print('PASS five balance sheets, cash/equity/insurance links, liquidity refusal,')
    print('     revolver interest, realization sensitivity, and negative-FCFE handling')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--break-cash', action='store_true')
    parser.add_argument('--export', action='store_true', help='write CSV, JSON and statement Markdown beside this script')
    args = parser.parse_args()
    if args.self_test:
        self_test()
        print('\n'+DISCLAIMER)
        return
    rows = project()
    if args.break_cash:
        rows[0]['corporate_cash'] -= 100
    v = value_equity(rows)
    print('KKR Lab 10 — simplified consolidated scenario, not company guidance\n')
    print(markdown_tables(rows))
    print('\nCHECK BLOCK')
    for r in rows:
        print(f"FY{r['year']}: balance gap {0.0 if abs(totals(r)[3])<TOL else totals(r)[3]:.6f}; "
              f"corporate cash headroom {r['corporate_cash']-ASSUMPTIONS['minimum_cash']:,.3f}; "
              f"revolver {r['revolver']:,.3f}; "+('negative FCFE' if r['fcfe']<0 else 'positive FCFE'))
    print(f"\nRemaining-cash-flow value on {VALUATION_DATE}: ${v['price']:.2f}/as-converted share")
    print(f"Equity value: ${v['equity']:,.3f} million; terminal share {v['terminal_share']:.2%}")
    print(f"Estimated excess corporate cash less revolver: ${v['excess_cash']:,.3f} million")
    print(f"Cost of equity {ASSUMPTIONS['cost_of_equity']:.3%}; shares {ASSUMPTIONS['shares']:.6f} million")
    print(f'Market snapshot: ${MARKET_PRICE:.2f}, {MARKET_TIMESTAMP}')
    if v['negative_years']:
        print(f"Negative FCFE: {v['negative_years']}; positive-only classroom value omits funding deficits.")
        print(f"Signed-cash-flow diagnostic: ${v['signed_price']:.2f}/share")
    if not v['terminal_supported']:
        print('Terminal value withheld: a negative final FCFE does not support a positive going-concern perpetuity.')
    if args.export:
        dest = Path(__file__).resolve().parent
        with (dest/'projected_statements.csv').open('w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
        (dest/'model_results.json').write_text(json.dumps(dict(valuation_date=str(VALUATION_DATE),
            market_price=MARKET_PRICE, market_timestamp=MARKET_TIMESTAMP,
            opening=OPENING, assumptions=ASSUMPTIONS, valuation=v, forecasts=rows), indent=2)+'\n')
        (dest/'PROJECTED_STATEMENTS.md').write_text('# KKR Lab 10 projected statements\n\n'
            'Generated by `python3 kkr_proforma.py --export`. Read Lab10_KKR.md for sources, '
            'assumptions, limitations and participation status. USD millions.\n\n'+markdown_tables(rows)+
            '\n\n## Disclaimer\n\n'+DISCLAIMER+'\n')
    print('\n'+DISCLAIMER)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, AssertionError) as exc:
        raise SystemExit(f'MODEL REFUSED: {exc}') from exc
