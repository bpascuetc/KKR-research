"""Shared SEC facts, three deterministic screens, separately authored model memos."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
for skill, module in [('buffett-edgar', 'scripts'), ('cathie-wood-edgar', 'scripts'), ('burry-edgar', 'scripts')]:
    sys.path.insert(0, str(ROOT / '.agents/skills' / skill / module))
import edgar
from cathie_checks import cathie_checks, configuration
from burry_checks import burry_checks

INVESTORS = ('Buffett', 'Cathie Wood', 'Burry')
EXTRA_TAGS = {'liabilities': 'Liabilities', 'research_and_development': 'ResearchAndDevelopmentExpense'}


def analyze(facts, ticker, config=None):
    result = edgar.analyze(facts, ticker)
    for row in result['rows']:
        for metric, tag in EXTRA_TAGS.items():
            options = edgar.candidates(facts, tag, row['fiscal_year_end'], instant=metric == 'liabilities')
            if options:
                f = max(options, key=lambda x: (x.get('filed', ''), x.get('accn', ''), x.get('start', '')))
                selected = {**{k: f.get(k) for k in ('val', 'start', 'end', 'filed', 'accn', 'form')},
                            'tag': 'us-gaap:' + tag, 'unit': 'USD'}
            else:
                selected = {'val': None, 'tag': 'not found', 'end': row['fiscal_year_end'], 'searched_tags': [tag]}
            row[metric] = selected['val']
            row['sources'][metric] = selected
        equity, revenue = row['equity'], row['revenue']
        row['liabilities_to_equity'] = None if row['liabilities'] is None or equity is None or equity <= 0 else row['liabilities'] / equity
        row['rd_percent'] = None if row['research_and_development'] is None or revenue is None or revenue <= 0 else row['research_and_development'] / revenue * 100
    wood = cathie_checks(result['rows'], config)
    burry = burry_checks(result['rows'])
    result['panel'] = {'Buffett': {'checks': result['checks']}, 'Cathie Wood': wood, 'Burry': burry}
    return result


def panel_table(result):
    return [{'Investor': investor, 'Check': name, 'Result': status}
            for investor, data in result['panel'].items() for name, status in data['checks'].items()]


def percent(value):
    return 'not known' if value is None else f'{value:.2f}%'


def ratio(value):
    return 'not known' if value is None else f'{value:.2f}'


def report(result):
    base = edgar.report(result).removesuffix(edgar.DISCLAIMER + '\n')
    # Original report keeps the full old table/provenance; the panel adds exact new inputs.
    lines = [base, '## Additional shared facts',
             '| FY end | Liabilities, USD millions | R&D, USD millions | R&D / revenue | Liabilities / equity |',
             '|---|---:|---:|---:|---:|']
    for row in result['rows']:
        lines.append('| ' + ' | '.join([row['fiscal_year_end'], edgar.money(row['liabilities']),
                     edgar.money(row['research_and_development']), percent(row['rd_percent']), ratio(row['liabilities_to_equity'])]) + ' |')
    wood = result['panel']['Cathie Wood']
    lines += [f"\nRevenue growth a year, first to last: {percent(wood['metrics']['revenue_growth_percent'])}.",
              'Formula: (last revenue / first revenue)^(1/4) - 1; five fiscal observations.',
              f"Active growth threshold: {wood['config']['growth_threshold_percent']:g}%; active R&D threshold: {wood['config']['rd_threshold_percent']:g}%.",
              'Burry leverage ceiling: 2 times positive equity.',
              '\n## Panel checks', '| Investor | Check | Result |', '|---|---|---|']
    for row in panel_table(result):
        lines.append(f"| {row['Investor']} | {row['Check']} | {row['Result']} |")
    lines += ['\nValues are not price valuations. Not found is not zero; not known is not pass.', edgar.DISCLAIMER]
    return '\n'.join(lines) + '\n'


def run(ticker, output_dir=None, user_agent='', offline=False, config=None):
    out = Path(output_dir or ROOT / 'evidence')
    # Reuse unchanged Lab18 downloader, ticker validation and output for compatibility.
    base = edgar.run(ticker, out, user_agent, offline)
    ticker = base['ticker']
    raw = (out / f'{ticker}_companyfacts.json').read_bytes()
    meta = out / f'{ticker}_companyfacts.source.json'
    if meta.exists() and json.loads(meta.read_text())['sha256'] != hashlib.sha256(raw).hexdigest():
        raise ValueError('SEC raw file hash does not match its download provenance.')
    result = analyze(json.loads(raw), ticker, config)
    result['raw_sha256'] = hashlib.sha256(raw).hexdigest()
    (out / f'{ticker}_panel_results.json').write_text(json.dumps(result, indent=2) + '\n')
    (out / f'{ticker}_panel_printed.md').write_text(report(result))
    return result


def memo_fingerprint(result, investor):
    payload = {'rows': result['rows'], 'investor': investor, 'screen': result['panel'][investor]}
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


def memo_path(result, investor, directory=None):
    suffix = investor.lower().replace(' ', '_')
    if investor == 'Cathie Wood':
        config = result['panel'][investor]['config']
        suffix += f"_{config['growth_threshold_percent']:g}_{config['rd_threshold_percent']:g}"
    return Path(directory or ROOT / 'memos') / f"{result['ticker']}_{suffix}.md"


def audit(result, directory=None):
    output = {}
    for investor in INVESTORS:
        path = memo_path(result, investor, directory)
        source = path.with_suffix('.source.json')
        output[investor] = {
            'memo_exists': path.exists(),
            'unsupported_numbers': edgar.unsupported_numbers(path.read_text(), report(result)) if path.exists() else None,
            'current': source.exists() and json.loads(source.read_text()).get('fingerprint') == memo_fingerprint(result, investor),
        }
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('ticker')
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'evidence')
    parser.add_argument('--offline', action='store_true')
    parser.add_argument('--user-agent', default=edgar.os.getenv('SEC_USER_AGENT', ''))
    parser.add_argument('--audit', action='store_true')
    args = parser.parse_args()
    try:
        result = run(args.ticker, args.output_dir, args.user_agent, args.offline)
        print(report(result))
        if args.audit:
            checks = audit(result)
            print(json.dumps(checks, indent=2))
            if not all(v['memo_exists'] and v['current'] and v['unsupported_numbers'] == [] for v in checks.values()):
                raise SystemExit(2)
    except (OSError, ValueError) as error:
        parser.exit(1, f'Error: {error}\n')


if __name__ == '__main__':
    main()
