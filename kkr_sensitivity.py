"""Lab 11 KKR sensitivity; standard library only; preserves the Lab 10 model.

Default: reproduce the base only. --run requires authorized ranges and a
pre-run prediction in sensitivity_inputs.json. No valuation function is called.
"""
import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import kkr_proforma as model

HERE = Path(__file__).resolve().parent
YEARS = list(range(2026, 2031))
TOL = model.TOL  # 0.000001 USD million = $1
DISCLAIMER = model.DISCLAIMER
UNAVAILABLE = ('Unavailable: parent cash allocation, accrued-carry realization and '
               'insurance remittance capacity remain unresolved in Lab 10. '
               'No terminal value or share value is calculated in Lab 11.')
# Only existing operating/reinvestment inputs; financing and valuation inputs excluded.
INPUTS = {
    'fee_growth': ('Fees-and-other annual growth', 'fraction per year'),
    'capital_income_growth': ('Capital-allocation income annual growth', 'fraction per year'),
    'insurance_growth': ('Insurance operating growth', 'fraction per year'),
    'overhead_growth': ('AM occupancy and cash G&A growth', 'fraction per year'),
    'compensation_ratio': ('AM compensation / AM revenue', 'fraction of AM revenue'),
    'depreciation_rate': ('AM depreciation / opening PP&E', 'fraction of opening PP&E'),
    'capex': ('FY2026 capital spending; existing capex-growth path retained', 'USD millions'),
    'capex_growth': ('Annual capital-spending growth', 'fraction per year'),
    'am_gain_yield': ('AM investment total gain yield', 'fraction of opening AM investments'),
    'gain_cash_fraction': ('Current AM gains realized in cash', 'fraction of current AM gains'),
    'carry_cash_fraction': ('Current capital-allocation income realized in cash', 'fraction of current capital-allocation income'),
    'am_dividend_yield': ('AM investment dividend yield', 'fraction of opening AM investments'),
    'am_interest_yield': ('AM investment interest yield', 'fraction of opening AM investments'),
    'insurance_yield': ('Insurance investment yield', 'fraction of opening insurance investments'),
    'policy_credit_rate': ('Policy credited-interest rate', 'fraction of opening policy liabilities'),
    'deposit_rate': ('Net policyholder deposit rate', 'fraction of opening policy liabilities'),
    'incremental_wc': ('Working capital / increase in fees', 'fraction of fee increase'),
    'common_retention': ('Insurance capital retention', 'fraction of positive common cash capacity'),
}


def read_json(path):
    return json.loads(path.read_text())


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def load_base():
    frozen = read_json(HERE / 'base_snapshot.json')
    actual = hashlib.sha256((HERE / 'kkr_proforma.py').read_bytes()).hexdigest()
    if actual != frozen['source_sha256']:
        raise ValueError('Lab 10 model snapshot changed; investigate before sensitivity')
    if model.ASSUMPTIONS != frozen['assumptions'] or model.OPENING != frozen['opening']:
        raise ValueError('Lab 10 default inputs differ from frozen base')
    return frozen


def run_once(base, overrides=None, backend=model):
    """Fresh copies of every independent input, including opening balances."""
    inputs, opening = deepcopy(base['assumptions']), deepcopy(base['opening'])
    inputs.update(overrides or {})
    expected_inputs, expected_opening = deepcopy(inputs), deepcopy(opening)
    result = dict(inputs=deepcopy(inputs), opening=deepcopy(opening), rows=[], valid=False,
                  error=None, operating_profit=None, fcfe=None, value_per_share=None)
    try:
        rows = backend.project(inputs, opening)
        result['rows'] = rows  # Preserve signed results, including failed checks.
        backend.check_rows(rows, inputs, opening)
        if inputs != expected_inputs or opening != expected_opening:
            raise ValueError('Model mutated independent inputs')
        result.update(valid=True, operating_profit=rows[-1]['revenue']-rows[-1]['expenses'],
                      fcfe=rows[-1]['fcfe'])
    except (ValueError, ArithmeticError) as exc:
        result['error'] = str(exc)
    return result


def validate_config(config, base):
    if config.get('years') != YEARS:
        raise ValueError('This unchanged scalar-input model applies each setting in FY2026–2030')
    drivers = config.get('drivers', [])
    if len(drivers) != 2 or len({d['key'] for d in drivers}) != 2:
        raise ValueError('Supply exactly two distinct selected operating drivers')
    for d in drivers:
        key = d['key']
        if key not in INPUTS:
            raise ValueError(f'{key} is not a supported existing operating input')
        if d.get('units') != INPUTS[key][1] or not d.get('reason', '').strip():
            raise ValueError(f'{key}: supply the stated units and the reason for the range')
        if d['base'] != base['assumptions'][key] or not d['lower'] < d['base'] < d['higher']:
            raise ValueError(f'{key}: require lower < exact saved base < higher')
        for level in ('lower', 'base', 'higher'):
            model.validate_inputs(dict(base['assumptions'], **{key: d[level]}), base['opening'])
    prediction = config.get('locked_prediction')
    if not prediction:
        raise ValueError('Pre-run prediction record is missing; no changed runs executed')
    for field in ('recorded_at', 'key', 'old', 'new', 'expected_direction', 'rough_size', 'why'):
        if field not in prediction or prediction[field] in ('', None):
            raise ValueError(f'Locked prediction is missing {field}')
    stamp = datetime.fromisoformat(prediction['recorded_at'].replace('Z', '+00:00'))
    if stamp.tzinfo is None or stamp > datetime.now(timezone.utc):
        raise ValueError('Prediction must have a past timezone-aware timestamp')
    selected = next((d for d in drivers if d['key'] == prediction['key']), None)
    if selected is None or prediction['old'] != selected['base'] or prediction['new'] not in (selected['lower'], selected['higher']):
        raise ValueError('Prediction must identify one selected change from its base')


def collect(base, drivers, backend=model):
    frozen = deepcopy(base)
    first = run_once(base, backend=backend)
    if not first['valid']:
        raise ValueError('Base run failed: ' + str(first['error']))
    runs = []
    for d in drivers:
        for level in ('lower', 'base', 'higher'):
            result = run_once(base, {d['key']: d[level]}, backend)
            changed = [k for k, v in result['inputs'].items() if v != base['assumptions'][k]]
            expected = [] if level == 'base' else [d['key']]
            if changed != expected or result['opening'] != base['opening']:
                raise ValueError('More than the selected independent input changed')
            result.update(key=d['key'], level=level, input_value=d[level], changed_keys=changed)
            for output in ('operating_profit', 'fcfe'):
                result['delta_' + output] = result[output]-first[output] if result['valid'] else None
            runs.append(result)
    restored = run_once(base, backend=backend)
    if base != frozen or restored != first:
        raise ValueError('Restored base does not exactly match original inputs and outputs')
    spans = []
    for d in drivers:
        valid = [r for r in runs if r['key'] == d['key'] and r['valid']]
        spans.append(dict(key=d['key'], valid_runs=len(valid), complete=len(valid) == 3,
            **{o: max(r[o] for r in valid)-min(r[o] for r in valid) if valid else None
               for o in ('operating_profit', 'fcfe')}))
    return dict(base=first, runs=runs, spans=spans, restored=restored, restored_exactly=True)


def fmt(number):
    return 'N/A' if number is None else f'{number:,.6f}'


def render(data, config):
    lines = ['# KKR Lab 11 — visible sensitivity output', '',
        'USD millions; outputs are FY2030E. Cash flow is signed common FCFE before revolver financing.',
        'Operating-profit proxy = consolidated revenue minus expenses, before net AM investment income.',
        'It retains insurance debt interest in expenses, matching Lab 10; it is not standardized EBIT or KKR FRE.',
        '', '**Value per share: ' + UNAVAILABLE + '**', '',
        '| Driver | Level | Actual input (model units) | Operating profit | Change from base | Common FCFE | Change from base | Checks |',
        '|---|---|---:|---:|---:|---:|---:|---|']
    for r in data['runs']:
        lines.append(f"| {r['key']} | {r['level']} | {r['input_value']:.12g} | {fmt(r['operating_profit'])} | {fmt(r['delta_operating_profit'])} | {fmt(r['fcfe'])} | {fmt(r['delta_fcfe'])} | {'PASS' if r['valid'] else 'INVALID: '+r['error']} |")
    lines += ['', 'All settings apply in each of FY2026–2030; capex is a FY2026 budget grown at the unchanged capex-growth rate.', '']
    for d in config['drivers']:
        lines.append(f"- `{d['key']}`: {INPUTS[d['key']][0]}; units: {d['units']}. Recorded range rationale (AI-assisted, authorized by Bernat): {d['reason']}")
    lines += ['', '| Driver | Valid runs | Operating-profit span | FCFE span |', '|---|---:|---:|---:|']
    for s in data['spans']:
        lines.append(f"| {s['key']} | {s['valid_runs']}/3 | {fmt(s['operating_profit'])} | {fmt(s['fcfe'])} |")
    lines += ['', 'Spans = maximum minus minimum across valid results. Invalid runs are excluded.',
              'No two-driver ranking is reported if either driver has an invalid run.']
    if all(s['complete'] for s in data['spans']):
        for o in ('operating_profit', 'fcfe'):
            largest = max(s[o] for s in data['spans'])
            leaders = [s['key'] for s in data['spans'] if abs(s[o]-largest) <= TOL]
            lines.append(f"Numerical largest {o} span over these ranges: {', '.join(leaders)} ({fmt(largest)} USD millions).")
    lines += ['', '## Restored base and accounting checks', '',
              'PASS: restored inputs and every statement cell exactly equal the first base run (stronger than $1 tolerance).',
              'Each usable run passes all original accounting links, cash-floor and borrowing-capacity checks.',
              'Accounting tolerance: 0.000001 USD million ($1); displayed rounding: 0.000001 USD million.',
              'Independent inputs reset from a fresh copy; only the listed driver changes. Opening balances stay fixed.', '']
    for r in [dict(data['base'], key='original', level='base'), *data['runs'], dict(data['restored'], key='restored', level='base')]:
        lines += [f"### {r['key']} / {r['level']}", '', '| Year | Balance gap | Cash headroom | Revolver | Signed common FCFE |', '|---|---:|---:|---:|---:|']
        for row in r['rows']:
            lines.append(f"| {row['year']} | {model.totals(row)[3]:+.9f} | {row['corporate_cash']-r['inputs']['minimum_cash']:.6f} | {row['revolver']:.6f} | {row['fcfe']:.6f} |")
    lines += ['', '## Locked prediction comparison', '',
              'Original AI-assisted pre-run record is preserved in `sensitivity_inputs.json` and `locked_inputs_used.json`.',
              'Prediction-error explanation, interpretation and partner exchanges belong in `STUDENT_RECORD.md`.']
    p = config['locked_prediction']
    chosen = next(r for r in data['runs'] if r['key'] == p['key'] and r['input_value'] == p['new'])
    lines += [f"Selected change: {p['key']} {p['old']} → {p['new']}; operating-profit change {fmt(chosen['delta_operating_profit'])}; FCFE change {fmt(chosen['delta_fcfe'])} USD millions.",
              '', '## Disclaimer', '', DISCLAIMER, '']
    return '\n'.join(lines)


def self_test():
    """Test plumbing on explicitly synthetic data, never on changed KKR inputs."""
    class Fake:
        @staticmethod
        def project(a, opening):
            # Nonlinear cross-term detects accidental carry-over between drivers.
            return [dict(revenue=a['x']*a['y'], expenses=opening['expense'], fcfe=a['x']-a['y'])]
        @staticmethod
        def check_rows(rows, a, opening):
            if a['x'] < 0:
                raise ValueError('Synthetic invalid scenario')
    base = dict(assumptions=dict(x=2., y=3.), opening=dict(expense=1.))
    drivers = [dict(key='x', lower=-1., base=2., higher=4.), dict(key='y', lower=2., base=3., higher=5.)]
    result = collect(base, drivers, Fake)
    assert not result['runs'][0]['valid'] and result['runs'][0]['rows'][0]['fcfe'] == -4.
    assert result['runs'][0]['delta_fcfe'] is None
    assert result['runs'][3]['operating_profit'] == 3.  # x reset to 2, not 4
    assert result['runs'][5]['fcfe'] == -3.  # signed cash retained
    assert result['runs'][5]['delta_fcfe'] == -2.
    assert result['spans'][0]['valid_runs'] == 2 and not result['spans'][0]['complete']
    assert result['spans'][1]['fcfe'] == 3.
    result['runs'][1]['inputs']['x'] = 999.
    assert result['base']['inputs']['x'] == base['assumptions']['x'] == 2.
    assert result['restored_exactly']
    print('PASS synthetic tests: fresh copies, independent reset, signed FCFE, invalid-run exclusion, deltas, spans, restored base.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', action='store_true', help='run authorized ranges after prediction is recorded')
    parser.add_argument('--self-test', action='store_true', help='synthetic plumbing tests; no changed KKR scenarios')
    args = parser.parse_args()
    if args.self_test:
        self_test()
        print('\n' + DISCLAIMER)
        return
    base = load_base()
    first = run_once(base)
    if not first['valid'] or first['rows'] != base['forecasts']:
        raise ValueError('Base does not match saved Lab 10 or fails checks')
    if not args.run:
        print('PASS: base inputs and all five forecast years exactly match saved Lab 10.')
        print(f"FY2030 operating-profit proxy: {first['operating_profit']:,.6f} USD millions")
        print(f"FY2030 signed common FCFE: {first['fcfe']:,.6f} USD millions")
        print('Value per share: ' + UNAVAILABLE)
        print('This command executes only the unchanged base. Use --run for the recorded ranges and locked prediction.')
        print('\n' + DISCLAIMER)
        return
    config = read_json(HERE / 'sensitivity_inputs.json')
    validate_config(config, base)
    # Freeze evidence before the first changed scenario; never silently replace a prior run.
    if (HERE / 'locked_inputs_used.json').exists():
        if read_json(HERE / 'locked_inputs_used.json')['config'] != config:
            raise ValueError('Inputs changed since previous run; preserve that run in a new dated folder first')
    else:
        write_json(HERE / 'locked_inputs_used.json', dict(frozen_at=datetime.now(timezone.utc).isoformat(), config=config))
    data = collect(base, config['drivers'])
    data.update(executed_at=datetime.now(timezone.utc).isoformat(), config=config,
                source_sha256=base['source_sha256'], valuation_unavailable_reason=UNAVAILABLE)
    write_json(HERE / 'sensitivity_results.json', data)
    output = render(data, config)
    (HERE / 'SENSITIVITY_OUTPUT.md').write_text(output)
    details = ['# KKR Lab 11 — statement details', '', 'USD millions. All signed cash flows retained. Value per share unavailable.', '']
    for r in [dict(data['base'], key='original', level='base'), *data['runs'], dict(data['restored'], key='restored', level='base')]:
        details += [f"# {r['key']} / {r['level']} — {'PASS' if r['valid'] else 'INVALID: '+r['error']}", '', model.markdown_tables(r['rows']) if r['rows'] else 'No statements: input/model failure.', '']
    details += ['## Disclaimer', '', DISCLAIMER, '']
    (HERE / 'STATEMENT_DETAILS.md').write_text('\n'.join(details))
    print(output)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, AssertionError) as exc:
        raise SystemExit(f'LAB 11 REFUSED: {exc}') from exc
