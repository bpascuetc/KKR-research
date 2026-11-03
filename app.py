"""Run: python -m streamlit run app.py"""
import hashlib
import json
import os
from pathlib import Path
import sys

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / '.agents/skills/buffett-edgar/scripts'))
from edgar import DISCLAIMER, TAGS, money, report, run, unsupported_numbers

st.set_page_config(page_title='Buffett · Business before price', layout='wide')
st.title('Buffett · Business before price')
st.caption('Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.')
st.write('A repeatable financial screen, followed by a Buffett-inspired judgment of the business.')
with st.sidebar:
    ticker = st.text_input('Ticker', 'COST').strip().upper()
    source = st.radio('Data source', ['Saved SEC download', 'Refresh from SEC'])
    name = st.text_input('Your name', 'Bernat Pascuet Cuesta')
    email = st.text_input('Your email (required for SEC refresh)', '')
    load = st.button('Load company', type='primary')
    st.caption('The saved download is reproducible. Refresh replaces its source files and results.')

if 'result' not in st.session_state:
    if (ROOT / 'evidence/COST_companyfacts.json').exists():
        st.session_state.result = run('COST', ROOT / 'evidence', offline=True)

if load:
    try:
        with st.spinner('Reading annual SEC facts…'):
            st.session_state.result = run(ticker, ROOT / 'evidence',
                                          user_agent=f'{name} {email}',
                                          offline=source == 'Saved SEC download')
    except Exception as error:
        st.session_state.pop('result', None)
        st.error(f'Could not load {ticker}: {error}')

if 'result' not in st.session_state:
    st.info('Enter a ticker and your SEC contact details, then load the company.')
    st.stop()

result = st.session_state.result
active = result['ticker']
printed = report(result)
st.subheader(f"{active} · {result['entity']}")
meta_path = ROOT / 'evidence' / f'{active}_companyfacts.source.json'
if meta_path.exists():
    meta = json.loads(meta_path.read_text())
    st.caption(f"SEC download: {meta['retrieved_at']} · {meta['url']}")
    actual_hash = hashlib.sha256((ROOT / 'evidence' / f'{active}_companyfacts.json').read_bytes()).hexdigest()
    if actual_hash != meta['sha256']:
        st.error('Saved raw facts no longer match the download hash. Refresh before relying on them.')

chart = pd.DataFrame([{'Fiscal year end': row['fiscal_year_end'],
                       'Owner earnings': None if row['owner_earnings'] is None else row['owner_earnings'] / 1e6,
                       'Net income': None if row['net_income'] is None else row['net_income'] / 1e6}
                      for row in result['rows']]).set_index('Fiscal year end')
st.line_chart(chart, y_label='USD millions', x_label='Fiscal year end')
if any(row['owner_earnings'] is None for row in result['rows']):
    st.warning('Owner earnings not found for one or more years. Missing observations are not zero.')

table = []
for row in result['rows']:
    table.append({'FY end': row['fiscal_year_end'], **{k.replace('_', ' ').title(): money(row[k]) for k in TAGS},
                  'ROE %': 'not known' if row['roe_percent'] is None else f"{row['roe_percent']:.1f}%",
                  'Owner earnings': money(row['owner_earnings'])})
st.caption('USD millions; ROE uses year-end equity. Owner earnings = operating cash flow − capital spending.')
st.dataframe(pd.DataFrame(table), hide_index=True, width='stretch')
st.subheader('The code checks')
st.dataframe(pd.DataFrame([{'Check': k, 'Result': v} for k, v in result['checks'].items()]),
             hide_index=True, width='stretch')
with st.expander('XBRL tags and selected filing evidence'):
    st.markdown(printed[printed.index('### Tags'):])
    st.download_button('Download script output', printed, f'{active}_printed.md')

st.subheader('The model judges')
memo_path = ROOT / 'memos' / f'{active}_memo.md'
original = memo_path.read_text() if memo_path.exists() else ''
memo = st.text_area('Memo — edit to test the number audit', original, height=300, key=f'memo_{active}')
if not original:
    st.info('No AI memo saved for this ticker. Run $buffett-edgar in Codex, then reload the app; the app does not fabricate a model judgment.')
if st.button('Insert unsupported ROE probe', key=f'probe_{active}'):
    st.session_state[f'probe_text_{active}'] = memo + '\n\nProbe: ROE was 40.0%.\n'
if f'probe_text_{active}' in st.session_state:
    memo = st.session_state[f'probe_text_{active}']
    st.caption('Probe text is appended below; clear the probe to return to the editor.')
    if st.button('Clear probe'):
        del st.session_state[f'probe_text_{active}']
        st.rerun()
flagged = unsupported_numbers(memo, printed)
if flagged:
    st.error('Numbers absent from script output: ' + ', '.join(flagged))
elif memo.strip():
    st.success('Every numeric token is present in the script output.')
st.caption('This checks numeric presence, not whether a printed number was assigned to the right metric, year or unit. Human review still matters.')
st.markdown(memo)
if memo:
    st.download_button('Download memo as Markdown', memo, f'{active}_memo.md')
    if st.button('Save edited memo'):
        memo_path.parent.mkdir(exist_ok=True)
        memo_path.write_text(memo)
        st.success(f'Saved {memo_path.name}; audit flags are retained above.')
st.divider()
st.caption(DISCLAIMER)
