# Lab19 — build request and source record

Bernat supplied the superseding November Legend Panel assignment. This implementation request is AI-assisted, based on that assignment:

> Extend my working Lab18 app and preserve its extraction, tables, owner-earnings chart, number audit and saved Buffett judgments. Add separate Cathie Wood and Burry skills based on their FAskills pages, applying the lab's exact coded checks to one shared five-year SEC dataset. Add only the prescribed Liabilities and ResearchAndDevelopmentExpense tags. Compute endpoint revenue CAGR over four intervals. Display the seven checks, each investor's saved verdict and three side-by-side memos; flag unprinted numbers in every memo. Reproduce COST without feeding anchors into extraction, change the growth threshold inside Cathie's skill to five percent and restore the chosen default. Use my Project2 fund's largest company and preserve every source gap. Prepare a code walkthrough, bull/bear discussion preparation, conditional trust decision and upload package without inventing personal participation or submissions.

## Sources used

- [Cathie Wood philosophy](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/cathie_wood.md): growth and innovation/reinvestment lens.
- [Michael Burry philosophy](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/michael_burry.md): skepticism about cash backing and balance-sheet risk.
- [SEC companyfacts API](https://www.sec.gov/search-filings/edgar-application-programming-interfaces): raw facts and filing provenance.
- [Streamlit columns](https://docs.streamlit.io/develop/api-reference/layout/st.columns): three-column display.
- Lab18 original raw COST/JPM SEC downloads, source hashes, extractor and Buffett memos; these were copied, not refreshed.
- `../../Lab15/2026-10-22/updated_app/project2_mandate.json`: existing student-confirmed VTI/BND/SGOV Project2 universe.

Only the FAskills philosophy pages were read. Their broader prompts for forecasts, prices, holdings, numerical scores and actual-investor impersonation are outside this lab's scope. FAskills software was not installed. The two new skills are adaptations, not claims of verbatim upstream installation. The superseded trading-strategy lab was not used.

I am a student, not a financial professional. This document was prepared for FIN 43900 (AI Finance Applications, Purdue) as a class learning exercise. It is not professional investment research or financial advice. I used OpenAI Codex to help with research, analysis, calculations, and drafting. Any remaining errors are my own.
