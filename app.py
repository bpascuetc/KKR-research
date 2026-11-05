"""Run: python -m streamlit run app.py --server.port 8503"""
import json
from pathlib import Path
import re

import pandas as pd
import streamlit as st

from panel import (INVESTORS, ROOT, audit, configuration, edgar, memo_fingerprint,
                   memo_path, panel_table, percent, ratio, report, run)

st.set_page_config(page_title='Legend Panel · Same facts, different lenses', layout='wide')
st.title('Legend Panel')
st.caption('Same SEC facts · Different questions · Human decision')
st.write('Buffett looks for earnings and owner cash. Cathie Wood screens growth and reinvestment. Burry checks cash backing and liabilities.')

with st.sidebar:
    ticker = st.text_input('Ticker', 'COST').strip().upper()
    source = st.radio('Data source', ['Saved SEC download', 'Refresh from SEC'])
    name = st.text_input('Your name', 'Bernat Pascuet Cuesta')
    email = st.text_input('Your email (required for SEC refresh)', '')
    load = st.button('Load company', type='primary')
    probe = st.checkbox('Probe Cathie Wood growth at 5%', value=False)
    st.caption('Probe changes only the growth hurdle. The skill configuration remains the kept default.')

config = configuration()
if probe:
    config = {**config, 'growth_threshold_percent': 5}
if 'result' not in st.session_state:
    try:
        st.session_state.result = run('COST', offline=True, config=config)
    except Exception as error:
        st.error(f'Could not open saved COST: {error}')
if load:
    try:
        with st.spinner('Reading annual SEC facts…'):
            st.session_state.result = run(ticker, user_agent=f'{name} {email}',
                                          offline=source == 'Saved SEC download', config=config)
    except Exception as error:
        st.session_state.pop('result', None)
        st.error(f'Could not load {ticker}: {error}')
if 'result' not in st.session_state:
    st.info('Load a company with a saved SEC download, or supply your SEC contact to refresh.')
    st.stop()

# Recompute screens when a skill configuration/probe changes, using the active company's facts.
result = st.session_state.result
if result['panel']['Cathie Wood']['config'] != config:
    try:
        result = run(result['ticker'], offline=True, config=config)
        st.session_state.result = result
    except Exception as error:
        st.error(f'Could not recompute panel: {error}')
        st.stop()
active = result['ticker']
printed = report(result)
st.subheader(f"{active} · {result['entity']}")
meta_path = ROOT / f'evidence/{active}_companyfacts.source.json'
if meta_path.exists():
    meta = json.loads(meta_path.read_text())
    st.caption(f"SEC download: {meta['retrieved_at']} · {meta['url']}")
st.caption(f"Growth {percent(result['panel']['Cathie Wood']['metrics']['revenue_growth_percent'])} · Active growth hurdle {config['growth_threshold_percent']:g}% · Latest liabilities/equity {ratio(result['panel']['Burry']['metrics']['latest_liabilities_to_equity'])}")
st.subheader('Panel checks')
st.dataframe(pd.DataFrame(panel_table(result)), hide_index=True, width='stretch')

st.subheader('Investor verdicts and memos')
st.caption('Saved AI classroom judgments using the printed evidence. These are simulations of investor lenses, not the investors’ actual opinions or independent factual confirmations.')
all_flags = {}
for investor, column in zip(INVESTORS, st.columns(3)):
    with column:
        st.markdown(f'### {investor}')
        path = memo_path(result, investor)
        original = path.read_text() if path.exists() else ''
        binding = path.with_suffix('.source.json')
        current = binding.exists() and json.loads(binding.read_text()).get('fingerprint') == memo_fingerprint(result, investor)
        key = f"memo_{active}_{investor}_{memo_fingerprint(result, investor)}"
        memo = st.text_area('Memo — edit to test the number audit', original, height=320, key=key)
        if not original:
            st.info('Memo not yet written. Use this investor skill on the printed output; the app does not invent a verdict.')
        elif not current:
            st.warning('This saved memo is stale for the active facts or thresholds. Review and rewrite it before trusting its verdict.')
        match = re.search(r'\*\*Verdict:\s*(.*?)\*\*', memo)
        if match:
            st.write(('Verdict: ' if current else 'Stale saved verdict: ') + match.group(1))
        if st.button('Insert unsupported ROE probe', key=f'probe_{active}_{investor}'):
            st.session_state[key + '_probe'] = True
        if st.session_state.get(key + '_probe'):
            memo += '\n\nProbe: ROE was 40.0%.\n'
            if st.button('Clear probe', key=key + '_clear'):
                del st.session_state[key + '_probe']
                st.rerun()
        flagged = edgar.unsupported_numbers(memo, printed)
        all_flags[investor] = flagged
        if flagged:
            st.error(f"{investor} — numbers absent from script output: " + ', '.join(flagged))
        elif memo.strip():
            st.success('Every numeric token is printed.')
        st.markdown(memo)
        if memo:
            st.download_button('Download memo', memo, path.name, key=key + '_download')
            if st.button('Save edited memo', key=key + '_save'):
                if flagged:
                    st.error('Correct unsupported numbers before saving this memo.')
                else:
                    path.write_text(memo)
                    binding.write_text(json.dumps({'fingerprint': memo_fingerprint(result, investor),
                                                   'author': 'User-edited memo; numeric presence checked'}, indent=2) + '\n')
                    st.success('Saved edited memo for the active facts and configuration.')
if any(all_flags.values()):
    st.error('Panel number audit flags: ' + '; '.join(f"{who}: {', '.join(flags)}" for who, flags in all_flags.items() if flags))
else:
    st.caption('Number audit covers all displayed memos. It checks numeric presence, not metric/year attribution or completeness of the analysis.')

with st.expander('Shared annual facts, chart and provenance', expanded=False):
    chart = pd.DataFrame([{'Fiscal year end': row['fiscal_year_end'],
                          'Owner earnings': None if row['owner_earnings'] is None else row['owner_earnings'] / 1e6,
                          'Net income': None if row['net_income'] is None else row['net_income'] / 1e6}
                         for row in result['rows']]).set_index('Fiscal year end')
    st.line_chart(chart, y_label='USD millions', x_label='Fiscal year end')
    if any(row['owner_earnings'] is None for row in result['rows']):
        st.warning('Owner earnings not found for one or more years. Missing observations are not zero.')
    table = []
    for row in result['rows']:
        table.append({'FY end': row['fiscal_year_end'],
                      **{k.replace('_', ' ').title(): edgar.money(row[k]) for k in [*edgar.TAGS, 'liabilities', 'research_and_development']},
                      'ROE': 'not known' if row['roe_percent'] is None else f"{row['roe_percent']:.1f}%",
                      'Owner earnings': edgar.money(row['owner_earnings']),
                      'R&D/revenue': percent(row['rd_percent']), 'Liabilities/equity': ratio(row['liabilities_to_equity'])})
    st.caption('Amounts in USD millions; ratios use unrounded source facts.')
    st.dataframe(pd.DataFrame(table), hide_index=True, width='stretch')
    st.markdown(printed)
    st.download_button('Download script output', printed, f'{active}_panel_printed.md')

st.divider()
st.caption(edgar.DISCLAIMER)
