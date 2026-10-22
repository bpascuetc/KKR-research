# Lab 15 — my individual checkout

Bernat Pascuet Cuesta · October 22, 2026

## My mandate and verification

I confirmed that Meridian is verified and that my Project 2 mandate is verified. My universe is VTI, BND and SGOV; my objective is an estimated annual return of at least 6.5%, with at least 3% in SGOV, long-only positions and full investment. The original Meridian input table is not bundled for local replay; my confirmation is recorded separately from the assistant's numerical execution.

## My evidence and stability results

My app imports portfolio.py; it uses one estimator and one search engine. My prices.csv contains 61 adjusted monthly price observations, September 2021–September 2026. price_sources.json records each ticker's source and October 22 download time. Return inputs are historical estimates, not forecasts.

On all 60 monthly returns, my lowest-risk feasible grid mix is **30% VTI / 0% BND / 70% SGOV**, with estimated return **6.54%** and volatility **4.85%**. On the last 36 monthly returns it becomes **15% VTI / 0% BND / 85% SGOV**, with estimated return **6.94%** and volatility **1.97%**. My largest weight change is **15 percentage points**.

Reducing VTI's estimated return by one percentage point changes the allocation to **35% VTI / 0% BND / 65% SGOV**: return estimate **6.66%**, volatility **5.64%**, and a **5-point** largest weight change. I do not lower the objective to force an allocation. Raising the reserve minimum to 8% leaves the selected base mix unchanged because the reserve constraint is slack. An incremental flat 25bp annual-cost assumption moves the mix to 35/0/65, with estimated return 6.76% after the assumed drag.

These are modeled estimates, not realized net backtest results. The cost stress is an assumption rather than a turnover-based estimate. Full output, convention details and feasibility counts are in updated_results.json and README.md.

## My AI claim dispositions

I accept the executed checks that weights sum to one, covariance calculations reconcile with directly weighted-return variance, and the grid respects its stated numerical objective and reserve constraint. I reject treating the lowest historical volatility, AI agreement or fund-weight caps as proof of full mandate compliance or future success. My confirmation of the mandate does not turn a historical mean into a forecast or replace implementation checks.

## My call and response to the executed stress

I would **reject adoption for now** and reconsider it in the future. My verified mandate remains unchanged, but the 15-point window sensitivity and 5-point one-point sensitivity show that my allocation depends materially on uncertain estimates. I would reconsider after fresh validation under the same mandate supports a mix whose sensitivity, feasibility and net performance I can defend.

“When I reduce VTI's expected annual return by one percentage point, my lowest-risk feasible mix moves from 30% VTI / 70% SGOV to 35% VTI / 65% SGOV, and estimated volatility rises from 4.85% to 5.64%. I would reject adoption for now because this sensitivity, together with the 15-point window change, makes the allocation sensitive to uncertain estimates; I would reconsider after further validation under my verified mandate.”

## My partner review

My partner used BIL, IEF, LQD and VT and also changed an estimate by one percentage point. We completed the partner attack and code explanation. His Accenture company work is separate from this four-fund portfolio exercise.

My response is: “A one-percentage-point change is useful because it tests whether the selected mix depends too heavily on a single uncertain estimate; I would compare the weights before and after the change rather than assume that the optimizer's first answer is reliable. In my own executed test, lowering VTI's return estimate by one point moved five percentage points into equities, and the 15-point change between estimation windows supports my decision to reject adoption for now and reconsider after further validation.”

This response uses my documented numerical results. It does not attribute those weights or results to my partner's different fund universe. His exact changed input, direction and resulting allocations were not supplied, so they are not invented here.

I would monitor reserve coverage, estimate/window sensitivity, implementation costs and mandate compliance at scheduled reviews. A changed constraint, loss of reserve eligibility or material validation failure would trigger reconsideration. No unsupported numerical loss guarantee or sensitivity tolerance is assumed.

## My personal entries and submission

I will complete my session token, teammates/learning partners, contribution, attendance declaration and truth attestation myself. I confirm that I completed the personal drawing, code explanation and partner attack. My partner uses BIL, IEF, LQD and VT. This completion record is based on my confirmation; the prepared walkthrough and Mermaid chart remain supporting materials rather than the original personal drawing.

I will upload the files to GitHub myself. My main links will be README.md, app.py, portfolio.py, prices.csv, price_sources.json and updated_results.json, with supporting inputs/tests alongside. I will enter the actual links in **Brightspace → Quizzes → Lab 15** and record the real receipt after submission. No upload or receipt is claimed here.

## My growth note

I can now gather and organize data more effectively and use it to make more informed, mature decisions. At this point, nothing feels particularly unclear.

I am a student, not a financial professional. This document was prepared for FIN 43900 (AI Finance Applications, Purdue) as a class learning exercise. It is not professional investment research or financial advice. I used OpenAI Codex to help with research, analysis, calculations, and drafting. Any remaining errors are my own.
