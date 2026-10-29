# Lab 17 — Point-in-Time Audit

Bernat Pascuet Cuesta | FIN 43900 | October 29, 2026

## Decision

**Quarantine DGS2 for Project 2 until the strategy enforces an as-of availability rule.** Then admit it only as a lagged rate-state input, using the ALFRED vintage for each decision date and observations published before the trade. Reconsider if the actual prework series differs, vintage coverage fails, units change, or a strategy needs intraday availability that daily vintages cannot establish. This is my AI-enhanced written decision. I completed the required Lab 17 oral discussion separately, including the activities specified as no AI.

DGS2 is a working selection for the VTI/BND/SGOV universe, not a claim that it was my previously chosen prework series. Short/intermediate Treasury rates can affect bond prices and the opportunity cost of equity; this is an economic rationale, not a tested predictive relationship. A yield level is not an ETF total return and must not replace adjusted fund returns in the Lab 15 optimizer. The existing portfolio app is preserved separately.

## Known-answer validation

All answers below were computed from public CSV downloads, not entered into app outputs. Observation dates of monthly series use the first day as a period label; September 1 does not mean September's full-month average was known on that day.

| Series | Last observation in October 5, 2026 vintage | Value | Result |
|---|---|---:|---|
| BAA | September 2026 | 6.47 | Pass |
| FEDFUNDS | September 2026 | 3.75 | Pass |
| DGS10 | October 2, 2026 | 5.28 | Pass |
| MORTGAGE30US | October 1, 2026 | 7.28 | Pass |

PAYEMS, as known January 15, 2025: latest measured month December 2024, 159,536 thousand jobs. Today's December 2024 value is 158,316 thousand, 1,220 thousand lower. Across common nonmissing observation dates from January 2020, 59 of 60 values are revised. There are 21 later monthly observations. This proves the two downloads contain different historical information sets; a latest-data date filter would miss revisions.

Download date: October 29, 2026. LIVE_AUDIT.json contains exact URLs, UTC retrieval times, CSV hashes, expected/actual checks and comparison results. The evidence folder preserves all 13 raw CSV responses.

## Data card — working series DGS2

| Field | Evidence / rule |
|---|---|
| ID and source | DGS2, Federal Reserve Board H.15, distributed by FRED/ALFRED; [FRED page](https://fred.stlouisfed.org/series/DGS2) |
| Measure | Market yield on US Treasury securities at 2-year constant maturity, quoted on an investment basis; interpolated constant-maturity yield, not the price or realized return of a particular bond |
| Units | Percent per annum, not seasonally adjusted; 4.67 means 4.67%, not 467%. Convert to 0.0467 only when a calculation calls for a decimal annual yield. Do not divide an annual yield by 12 and call it an observed monthly total return. |
| Frequency | Daily business-date observations; weekends/holidays may be absent or missing. A dot is missing, never zero. No filling in the audit. |
| Publication / lag | [H.15](https://www.federalreserve.gov/releases/h15/) is posted weekdays at 4:15 p.m., excluding holidays/closures. The October 29 page and FRED show October 28 as the latest observation, so this snapshot exhibits a one-calendar-day measurement-to-publication lag. Do not treat the observation date as availability or assume this lag is universal. |
| Vintage coverage | ALFRED selects values available on a requested calendar date. Its [help](https://alfred.stlouisfed.org/help) says additions typically follow source releases within one business day. A calendar vintage does not certify availability before a particular trading time. |
| Revisions | Zero revised common dates in the tested September 30 versus current window, across 1,687 dates. This is an empirical result for this window, not a guarantee that corrections never occur. |
| Download date | October 29, 2026; exact UTC times and SHA-256 hashes are in LIVE_AUDIT.json. |
| As-of rule | For daily decisions, use the prior calendar-date vintage as a conservative default, then the latest valid observation in that vintage. For month-end decisions, apply the same pre-trade rule; do not use later month-end measurements merely because their observation label is in that month. Intraday strategies need actual release-time evidence. |

### My-series experiment

Start date is January 1, 2020 for both comparisons.

| As known on | Last measured date | Value | Current last date / value | Later observations | Revised common dates |
|---|---|---:|---|---:|---:|
| September 30, 2026 | September 29, 2026 | 4.89 | October 28 / 4.67 | 20 | 0 |
| October 29, 2026 | October 28, 2026 | 4.67 | October 28 / 4.67 | 0 | 0 |

At September 30 the subsequent 20 observations were absent; they were not available for that decision. No revisions were detected on the common dates, so the demonstrated DGS2 risk is availability lag rather than a measured revision effect.

### Three source comparisons

I answered the three-value item, and Codex enhanced the wording of my response. The source comparison below was performed by Codex against the visible FRED page and Federal Reserve H.15 table on October 29; all three values match. My statement that I answered the item does not separately establish that I personally inspected the source page.

| Observation date | CSV | FRED page / H.15 |
|---|---:|---:|
| October 26, 2026 | 4.68 | 4.68 |
| October 27, 2026 | 4.70 | 4.70 |
| October 28, 2026 | 4.67 | 4.67 |

## Fresh eyes — earlier Accenture feedback and my response

My partner's company is Accenture. In our actual September 29 Lab 11 exchange, my partner asked what historical series and years supported my KKR growth range, whether the fee line contained less repeatable items, and whether changing the tested range could reverse the sensitivity ranking. Those comments are recorded in `Lab11/2026-09-29/PARTNER_EXCHANGE.md`; they are earlier feedback, not a quotation from Lab 17. I also completed the Lab 17 oral partner activities, including the required no-AI explanation and question exchange. My partner also gave feedback and asked questions orally during that completed Lab 17 exchange. Their exact wording is not reproduced here.

I apply the same evidence-first reasoning here: a field's label and a plausible economic story do not establish its scope or availability. The Accenture growth-to-FCFE bridge we discussed was +533.4 −190.3 +77.1 −27.3 −113.2 = +279.7 million; checking that arithmetic supported the stated cash bridge, but it did not establish when a FRED observation was published or whether its history was later revised.

### My two-sentence response on publication timing — AI-enhanced preparation

The September 30 DGS2 vintage ends at September 29 at 4.89%, while today's file includes 20 later observations, so using today's complete series on the earlier decision date would introduce unavailable information. I would quarantine the input until Project 2 uses a pre-trade vintage rule, and I would require release timestamps before admitting intraday use even though this comparison found no revisions on common dates.

This is my prepared response to a publication-timing challenge. I completed the actual Lab 17 oral exchange, including my partner’s feedback and questions and my answers; its exact wording was not supplied for this report. This written response was enhanced with AI; I do not present it as a verbatim transcript or attribute invented words to my partner.

## Learning and reflection — AI-enhanced preparation

A data card is an auditable description of what a series measures, its source, units, observation frequency, publication lag, revision behavior, retrieval date and usable information set. Publication and vintage fields stop an availability leak; unit checks stop a measurement error; revision checks stop later estimates from masquerading as earlier knowledge. “Cleaned the data” says nothing about those properties or whether the original data were knowable before a trade.

For DGS2, a latest-data backtest that reads each yield on its observation date can give the strategy information earlier than it was released. It may overstate timeliness and apparent predictive usefulness; the audit alone cannot prove how much portfolio return would change or that the direction of performance bias is always positive. For PAYEMS, latest-data history also substitutes revised estimates for what was originally known.

I confirm that I answered the three-value item; Codex enhanced the written response and performed the documented source comparisons. I confirm that I completed the Lab 17 oral activities: the opener, the no-AI line-by-line explanation and question swap, the partner discussion and the oral reflection. These were oral activities, not written transcripts; the AI-enhanced text here is subsequent written preparation. My personal inspection of the three source-page values is not separately confirmed. Checkout and submission are not established by these oral activities. Github links and Brightspace submission remain my responsibility.

I am a student, not a financial professional. This document was prepared for FIN 43900 (AI Finance Applications, Purdue) as a class learning exercise. It is not professional investment research or financial advice. I used OpenAI Codex to help with research, analysis, calculations, and drafting. Any remaining errors are my own.
