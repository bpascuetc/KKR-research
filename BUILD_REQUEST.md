# Lab18 — build request and source rules

Request prepared with Codex from Bernat's supplied assignment, rather than claimed as unaided writing:

> Build a discoverable Codex skill called buffett-edgar and a Streamlit app. Read Buffett's FAskills page for philosophy only; never install its software or use its data sources. Download ticker-to-CIK and companyfacts JSON directly from SEC EDGAR with my name and real email in the User-Agent. Select the last five fiscal-year-end dates, only annual USD 10-K flows and year-end equity, applying the assignment's exact tags, ordered fallbacks and latest-filing rule. Compute ROE, the lab owner-earnings proxy and its three checks in Python. Print provenance and missing-data labels. Use only printed numbers to write a short Buffett-inspired business-quality memo, without price data. Chart owner earnings and net income, show the table/checks/memo, and flag every memo number absent from the printed output. Verify the COST known answer without hard-coding it into extraction, probe JPM's missing capex and inject an unsupported ROE. Preserve raw downloads and test evidence. Prepare files for my GitHub upload.

Sources read:

- [Buffett philosophy](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/warren_buffett.md): business durability and owner cash guide the qualitative judgment. The lab formula takes precedence over the source's broader maintenance-capex formulation. No FAskills installation, prices or paid feeds.
- [Codex skills documentation](https://developers.openai.com/codex/skills): manifest, progressive disclosure, local discovery and explicit invocation. The page currently redirects to ChatGPT Learn; its location table includes `~/.agents/skills` and project `.agents/skills`.
- [SEC APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces): keyless companyfacts data and original filing provenance.
- [Streamlit chart API](https://docs.streamlit.io/develop/api-reference/charts/st.line_chart): chart rendering from the computed dataset.

The supplied prework page has a relative URL only; its contents were not provided or independently located. No claim that the prework was read is made.

I am a student, not a financial professional. This document was prepared for FIN 43900 (AI Finance Applications, Purdue) as a class learning exercise. It is not professional investment research or financial advice. I used OpenAI Codex to help with research, analysis, calculations, and drafting. Any remaining errors are my own.
