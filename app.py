"""Streamlit view. Every estimate and mix comes from portfolio.py."""
import json
from pathlib import Path
import pandas as pd
import altair as alt
import streamlit as st
from portfolio import load_meridian, load_proxy, covariance, estimate, search, largest_change

P=Path(__file__).resolve().parent
st.set_page_config(page_title='Portfolio Stability Decision', page_icon='📊', layout='wide')
st.title('Portfolio Stability Decision')
st.caption('Built with AI help — a learning demonstration, not investment advice.')
st.write('Find the lowest-volatility mix on a 5-percentage-point grid, then test how much it moves when an estimate changes.')
mode=st.sidebar.radio('Universe', ['Meridian training','My fund prices','Four-sleeve practice'], index=1 if (P/'prices.csv').exists() else 0)
objective=st.sidebar.number_input('Expected return objective (%)', value=6.5, step=.1)/100
reserve=st.sidebar.number_input('Minimum reserve-eligible weight (%)', min_value=0., max_value=100., value=3., step=1.)/100
upload=st.sidebar.file_uploader('Upload prices.csv (monthly adjusted closes)',type=['csv'])
last36=st.sidebar.checkbox('Use last 36 monthly returns',value=False)

try:
    if mode in ('Meridian training','Four-sleeve practice'):
        data=load_proxy() if mode=='Four-sleeve practice' else load_meridian()
        if mode=='Four-sleeve practice':
            st.warning('Market-proxy practice only: SGOV / IEF / LQD / VTI historical estimates. These are not the original course table and do not verify Meridian’s known answers.')
            st.caption('Bills / note / IG / equity are proxy sleeve labels. ETF reserve eligibility is a practice assumption. Data: September 2021–September 2026 adjusted prices.')
        original=data
        cov=covariance(data['volatilities'],data['correlations'])
        baseline_mu=data['returns']
        reference_note='Four-sleeve market-proxy estimates as loaded' if mode=='Four-sleeve practice' else 'Meridian inputs as loaded'
    else:
        if upload is None and not (P/'prices.csv').exists():
            st.info('Upload your 3–6 fund adjusted-price CSV and enter your own mandate objective/reserve rule. Do not lower the objective to force a mix.')
            st.stop()
        if upload is None:
            raw=(P/'prices.csv').read_bytes()
            st.caption('Using bundled VTI/BND/SGOV adjusted prices. Upload another CSV to replace them.')
        else:
            raw=upload.getvalue()
        original=estimate(raw,False)
        data=estimate(raw,last36)
        cov=data['covariance']
        baseline_mu=original['returns']
        reference_note='All-month CSV estimates with the current reserve selections'
        st.caption(f"Historical estimates, not forecasts. {data['observations']} monthly returns, prices {data['price_start']} to {data['price_end']}. Sample covariance, annualized ×12.")
        if data['price_rows'] not in (60,61):
            st.warning(f"Uploaded {data['price_rows']} price rows. The assignment requests five years; confirm the intended window and source metadata.")
    labels=data['labels']
    # Reset edited returns when the source, mode or estimation window changes.
    signature=json.dumps({'mode':mode,'labels':labels,'returns':data['returns'],'cov':data['correlations']},sort_keys=True)
    defaults=data.get('reserve_eligible',[False]*len(labels))
    if mode=='My fund prices' and labels==['VTI','BND','SGOV']:
        defaults=[False,False,True]
        st.info('Student-confirmed Project 2 mandate: 6.5% return objective and at least 3% SGOV reserve weight. VTI / BND / SGOV. Review eligibility against the actual mandate before investing.')
    st.subheader('Your estimates and reserve eligibility')
    st.caption('Expected returns are editable estimates. Reserve eligibility must follow the mandate; checking a box does not verify it.')
    mu=[]; eligible=[]
    for i,label in enumerate(labels):
        left,right=st.columns([3,2])
        mu.append(left.number_input(f'{label}: expected annual return (%)',value=float(data['returns'][i]*100),step=.1,key=f'mu-{signature}-{i}')/100)
        eligible.append(right.checkbox(f'{label}: reserve eligible',value=bool(defaults[i]),key=f'reserve-{mode}-{label}'))
    result=search(mu,cov,eligible,objective,reserve)
    refcov=covariance(original['volatilities'],original['correlations'])
    reference=search(baseline_mu,refcov,eligible,objective,reserve)
    def show_mix(col,title,value):
        col.subheader(title)
        if value is None:
            col.warning('No mix meets the objective and reserve rule.')
            return
        col.dataframe(pd.DataFrame({'Asset':labels,'Weight (%)':[round(v*100,2) for v in value['weights']]}),hide_index=True)
        col.write(f"Expected return: **{value['return']*100:.2f}%** · Volatility: **{value['volatility']*100:.2f}%**")
        col.write(f"Reserve-eligible weight: **{value['reserve_weight']*100:.2f}%**")
        col.caption(f"{value['feasible_mixes']:,} feasible mixes out of {value['grid_mixes']:,} grid mixes.")
    left,right=st.columns(2)
    show_mix(left,'Current lowest-risk mix',result)
    show_mix(right,'Inputs as loaded',reference)
    st.caption(reference_note)
    change=largest_change(result,reference)
    if change is None:st.info('Largest weight change: unavailable because at least one case has no feasible mix.')
    else:st.metric('Largest weight change',f'{change:.2f} percentage points')
    chart_cases=[('Current mix',result),('As loaded',reference)]
    feasible_cases=[(name,value) for name,value in chart_cases if value is not None]
    if feasible_cases:
        st.subheader('Portfolio comparison')
        weights_chart=pd.DataFrame([{'Asset':label,'Case':name,'Weight (%)':100*weight}
            for name,value in feasible_cases for label,weight in zip(labels,value['weights'])])
        risk_chart=pd.DataFrame([{'Case':name,'Annual volatility (%)':100*value['volatility'],
            'Annual return estimate (%)':100*value['return']} for name,value in feasible_cases])
        c1,c2=st.columns(2)
        allocation=(alt.Chart(weights_chart).mark_bar().encode(
            x=alt.X('Asset:N',sort=labels,title='Asset'),
            xOffset=alt.XOffset('Case:N'),
            y=alt.Y('Weight (%):Q',scale=alt.Scale(domain=[0,100]),title='Portfolio weight (%)'),
            color=alt.Color('Case:N',scale=alt.Scale(domain=['Current mix','As loaded'],range=['#2563eb','#f59e0b'])),
            tooltip=['Asset:N','Case:N',alt.Tooltip('Weight (%):Q',format='.2f')]).properties(title='Allocation: current versus as loaded'))
        points=(alt.Chart(risk_chart).mark_circle(size=160,opacity=.75).encode(
            x=alt.X('Annual volatility (%):Q',scale=alt.Scale(zero=True),title='Annual volatility estimate (%)'),
            y=alt.Y('Annual return estimate (%):Q',scale=alt.Scale(zero=False),title='Annual return estimate (%)'),
            color=alt.Color('Case:N',scale=alt.Scale(domain=['Current mix','As loaded'],range=['#2563eb','#f59e0b'])),
            shape='Case:N',tooltip=['Case:N',alt.Tooltip('Annual volatility (%):Q',format='.2f'),alt.Tooltip('Annual return estimate (%):Q',format='.2f')]))
        target=(alt.Chart(pd.DataFrame({'Objective (%)':[objective*100]})).mark_rule(strokeDash=[5,5],color='#64748b').encode(y='Objective (%):Q'))
        c1.altair_chart(allocation,width='stretch')
        c2.altair_chart((points+target).properties(title='Risk and return estimates; dashed objective'),width='stretch')
        st.caption('Charts show computed feasible mixes under the selected assumptions. Identical current and reference points overlap; changing a return estimate or the 36-month switch separates them. Hover to inspect exact values.')
    st.warning('This search enforces only full investment, long-only, the return estimate threshold and reserve-eligible minimum. It does not certify issuer limits, liquidity, turnover, costs, distributions or a loss guarantee. The 5-point grid may miss feasible off-grid allocations.')
    payload={'mode':mode,'inputs':data,'edited_returns':mu,'reserve_eligible':eligible,'objective':objective,'reserve_minimum':reserve,'current':result,'as_loaded':reference,'largest_weight_change_pp':change}
    st.download_button('Download this decision evidence',json.dumps(payload,indent=2),'decision_evidence.json','application/json')
    with st.expander('Estimates and correlations'):
        st.dataframe(pd.DataFrame({'Asset':labels,'Annual volatility estimate (%)':[100*v for v in data['volatilities']]}),hide_index=True)
        st.dataframe(pd.DataFrame(data['correlations'],index=labels,columns=labels))
except (ValueError,KeyError,TypeError,json.JSONDecodeError) as exc:
    st.error(str(exc))
    if mode=='Meridian training':
        st.info('Bernat confirms Meridian was verified. The original course table is not bundled, so this local mode cannot replay that verification yet. Select My fund prices to check the confirmed Project 2 mandate, or Four-sleeve practice for the separate market-proxy exercise.')

st.divider()
st.caption('I am a student, not a financial professional. This document was prepared for FIN 43900 (AI Finance Applications, Purdue) as a class learning exercise. It is not professional investment research or financial advice. I used OpenAI Codex to help with research, analysis, calculations, and drafting. Any remaining errors are my own.')
