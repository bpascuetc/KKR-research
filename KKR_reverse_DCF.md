# Lab 05 — KKR valuation, sensitivity and reverse DCF

Bernat Pascuet Cuesta · FIN 43900, AI Finance Applications · September 10, 2026

**Conditional class call: WATCH–DEFER.** The illustrative KKR case values a share at **$68.92**, versus the selected same-day quote of **$100.87**. Matching that quote requires a **+13.1892-percentage-point shift** to each 15% annual FCFF growth assumption, yielding **28.1892% in Years 1–5**. These are conditional calculations, not evidence that the market is wrong.

## Submission and reproduction

Upload **this document and [dcf.py](dcf.py)** together in the same folder. The Python file is self-contained and uses only the standard library. No Excel workbook or second Python file is required.

From this dated submission folder (`KKR-research/2026-09-10/`):

```bash
python3 dcf.py
python3 dcf.py --kkr
```

Each command prints the same twelve base-output lines, then the sensitivity grid, then the reverse DCF and held-fixed inputs. The first command retains the labeled training case because the classroom FCFF reconciliation and empirical WACC remain unresolved. The second runs an **illustrative KKR adaptation**, not training values relabeled as company data. The training example validates the arithmetic; it does not prescribe KKR's numbers. If Python is available as `python`, that command works too.

## Inputs, evidence and unresolved items

All model dollar amounts and shares are in **millions**, except dollars per share. Financial inputs are as of June 30, 2026; earnings inputs cover the trailing twelve months. Estimates below were adopted for this September 10 exercise. The main source is [KKR's July 30, 2026 earnings release and supplement](https://ir.kkr.com/media/document/15a25fa9-8226-4da1-9ff3-027b9803d436/assets/KKR_Q226_Earnings_Release.pdf?disposition=inline) (**S1**). Page references are printed page numbers, not PDF viewer page indices.

| Input | KKR case value | Locator, date and status |
|---|---:|---|
| Starting FCFF | 2,258.094300 | **Estimate**, not reported FCFF. S1 p.34, LTM June 2026: (FRE 4,235.479 + realized carry 703.508 − equity compensation 637.855) × 75% × 70%. Tax 25% and cash conversion 70% are assumptions. |
| Annual FCFF growth, Years 1–5 | 15%, 15%, 15%, 15%, 15% | **Forecast estimate**, September 10. S1 p.2 reports LTM FRE growth of 19%; 15% is a deliberately lower illustrative path, not management's FCFF guidance. Carry and reinvestment can make FCFF behave differently. |
| WACC | 11% | **Scenario; empirical estimate unresolved.** September 10 assumption: 90% equity at 11.75% plus 10% debt at 5.5% after 25% tax = 10.9875%, rounded. These costs and weights are not sourced market measurements. |
| Terminal growth | 3% | **Estimate**, September 10: long-run nominal growth assumption, below WACC. It is not an extrapolation of KKR's 15% forecast. |
| Non-operating cash | 4,314.264 | S1 p.36, June 30 segment cash 5,314.264 less **assumed** operating reserve 1,000. |
| Debt | 9,298.541 | S1 p.36, June 30 parent-issued/guaranteed debt at par. Insurance and consolidated fund debt are not subtracted again. |
| Reported diluted weighted-average shares | 945.581938 | S1 p.1, Q2 2026 GAAP earnings table; provided for the assignment's EPS share-count check. |
| Valuation shares used | 945.131511 | **Adaptation:** S1 p.33, June 30 adjusted shares 923.731511 + potential preferred conversion 21.4. Retains the prior KKR model's compensation expense and forward conversion convention. It is not the GAAP weighted-average denominator. |
| Other equity value | 22,845.565810 | Fixed sum of separately valued assets less other claims; full bridge below. Mixed reported inputs and estimates, June 30 base / September 10 assumptions. |
| Target share price | $100.87 | [Stock Analysis overview](https://stockanalysis.com/stocks/kkr/), labeled September 10, 2026, 4:00 p.m. EDT close, checked September 10 (**S2**). See quote discrepancy below. |
| Grid | WACC 10%, 11%, 12%; terminal growth 2%, 3%, 4% | September 10 scenario design: base assumptions at the centre. Every other input stays fixed. |
| Shift search bounds | −5 to +20 percentage points | September 10 numerical search choice; initial −5 to +10 bracket does not contain a KKR solution. Expanding the search changes no economic assumption. |

**Why this differs from a conventional company:** KKR combines asset management, insurance and investment holdings. Consolidated operating cash flow plus after-tax interest less capital expenditure has not been reconciled into a clean parent FCFF measure here. The adjusted FCFF proxy and separate equity bridge are an explicitly labeled extension. An empirical WACC estimate and a fully reconciled dilution treatment also remain open. The assignment permits unresolved inputs to be labeled and the training result retained; this document does not claim those gaps have disappeared.

The default training inputs are FCFF 100; annual growth 8%, 6%, 5%, 4%, 3%; WACC 10%; terminal growth 3%; cash 50; debt 300; shares 50; target $30. Their source is the supplied Lab 05 screenshots. They are **training placeholders only**, not KKR financial statements.

**Quote discrepancy:** S2 shows $100.87, while its [historical table](https://stockanalysis.com/stocks/kkr/history/) showed $100.79 for September 10 when checked. We select the timestamped overview quote transparently; the official closing-price reconciliation remains unresolved. The $0.08 discrepancy is about 0.08%, much smaller than the model uncertainty. No September 8 quote is presented as today's price.

## Fixed KKR equity bridge

| Component | USD millions | Evidence / assumption |
|---|---:|---|
| Principal investments after tax haircut | 7,961.965 | S1 p.36: 8,611.965 at June 30 less assumed tax haircut 650. |
| Global Atlantic equity | 11,799.440 | S1 p.36 June 30 adjusted book value × assumed 1.0 multiple. Insurance liabilities remain within this equity value. |
| Strategic Holdings equity | 3,554.516436 | S1 p.34 LTM net dividends 186.821; assume 25% tax, 20% dividend growth for five years, 3% thereafter and 11% equity discount rate. |
| Remaining preferred dividends | (220.355626) | S1 p.34 LTM dividends 161.719; assume six quarterly payments discounted at 11.75%. Preferred principal is not also deducted under the conversion convention. |
| Settlement reserve | (250.000) | Prior model assumption based on the [August 26 proposed DOJ settlement](https://www.justice.gov/opa/pr/kkr-agrees-pay-record-250m-penalty-serial-violations-federal-premerger-review-law); assume still unpaid. |
| **Other equity value** | **22,845.565810** | Sum of the five rows above, held fixed in every grid cell and reverse solve. |
| Plus non-operating cash, less debt | (4,984.277) | 4,314.264 − 9,298.541. |
| **Net equity bridge** | **17,861.288810** | Added to asset-management enterprise value. |

For reproduction, the Holdings value is the sum of five discounted dividends plus a year-five Gordon terminal value. Preferred value is `sum((161.719/4)/(1.1175)**(q/4) for q in range(1,7))`. Bridge values are stored as a fixed scenario snapshot in `dcf.py`. June balances are not fully rolled forward; acquisitions, commitments, contingent claims and changes in holdings may alter the bridge. Accrued carry is not added separately because projected FCFF includes realized carry.

## Training verification — completed before the company run

The original twelve training lines were compared with the pre-edit output and are unchanged. Base value is **$27.4974**. All nine rounded grid cells match the supplied example:

| WACC / terminal growth | 2% | 3% | 4% |
|---|---:|---:|---:|
| 9% | 28.60 | 32.94 | 39.02 |
| 10% | 24.36 | **27.50** | 31.69 |
| 11% | 21.06 | 23.41 | 26.44 |

Training target $30 produces **+1.7779 percentage points** on each annual rate. Starting FCFF, WACC, terminal growth, cash, debt, shares and the five-year horizon remain fixed. This matches the example's approximate +1.78 points.

Checks also passed for invalid terminal-growth cells, rejection of brackets reaching −100% annual growth, unreachable targets, KKR grid direction and reproduction of the KKR target to within $0.00000001.

## KKR base valuation — the twelve lines

```text
FCFF Year 1 (USD millions): 2596.8084
FCFF Year 2 (USD millions): 2986.3297
FCFF Year 3 (USD millions): 3434.2792
FCFF Year 4 (USD millions): 3949.4210
FCFF Year 5 (USD millions): 4541.8342
PV of five explicit FCFF (USD millions): 12571.3181
Terminal value at Year 5 (USD millions): 58476.1153
PV of terminal value (USD millions): 34702.7283
Enterprise value (USD millions): 47274.0464
Equity value (USD millions): 65135.3352
Value per diluted share (USD): 68.9167
PV of terminal value / enterprise value (fraction): 0.7341
```

Enterprise value above covers the asset-management FCFF stream. Equity value includes the separate fixed bridge. The denominator is the disclosed forward dilution convention, rather than reported GAAP weighted-average diluted shares.

## KKR sensitivity grid and range

| WACC / terminal growth | 2% | 3% | 4% |
|---|---:|---:|---:|
| 10% | 70.62 | 76.48 | 84.30 |
| 11% | 64.52 | **68.92** | 74.57 |
| 12% | 59.65 | 63.05 | 67.29 |

The base case is in the centre. Values **fall going down** as WACC rises and **rise going right** as terminal growth rises. The opposite corners give a **$59.65–$84.30 scenario range**, not a confidence interval. All nine cells hold the explicit cash flows, share count and complete equity bridge fixed. Cells with terminal growth greater than or equal to WACC are printed as `INVALID`.

## KKR reverse DCF — solve a uniform shift

```text
FCFF_t = starting_FCFF × product(1 + original_growth_i + shift), i = 1..t
Terminal_value = FCFF_5 × (1 + terminal_growth) / (WACC − terminal_growth)
Price = (PV of FCFF_1..5 + PV of Terminal_value + net_equity_bridge) / shares
```

Bisection solves **one shift**, not five independent growth rates. Within the initial −5 to +10-point bracket, **there is no solution**. In the disclosed wider −5 to +20-point bracket, the answer is **+13.1892 percentage points**, producing **28.1892% annual FCFF growth in each of Years 1–5** and reproducing **$100.870000**.

**Held fixed:** starting FCFF 2,258.094300; WACC 11%; terminal growth 3%; cash 4,314.264; debt 9,298.541; other equity value 22,845.565810; shares 945.131511; five annual periods; original growth-path differences; year-end discounting. The reverse solve does not recompute the starting FCFF proxy or reinvestment when growth changes. Higher growth without a changing reinvestment allowance is a limitation of this classroom exercise.

**Difference from the earlier report:** the previous $79.41 value and 26.04% reverse growth came from a different model and a September 8 price. That model increased terminal cash conversion from 70% to 90% and tied reinvestment to solved operating-profit growth. This version keeps starting FCFF fixed, applies a uniform growth shift and uses the classroom terminal formula. Its lower $68.92 base is principally due to removing the terminal cash-conversion step; the numbers were not adjusted to fit the share price. The earlier model is supplemental analysis, not the submission calculation.

## Reasonableness and the input I distrust most

**$68.92 / $100.87 = 0.683×**, inside the required **0.5×–2× band**. The model value is **31.7% below** the selected quote. Passing this broad band is a plausibility check, not validation of the valuation.

**I distrust starting FCFF most.** It is a proxy formed from adjusted earnings and assumed 70% conversion, not a reconciled statement-of-cash-flows measure. Realized carry is cyclical, and tax, compensation and reinvestment estimates materially influence available cash. About 73.4% of asset-management enterprise value comes from the terminal value. I have kept the assumptions unchanged rather than adjusting them to fit the quote.

## Conditional class call and monitoring

**Watch–defer. Initiate in the class scenario if price falls to $68.92 or below and the sourced evidence still supports the 15% forecast path; otherwise defer.** An alternative reason to revisit the call would be sourced evidence supporting roughly 28.19% annual FCFF growth under the fixed assumptions. Before treating either trigger as actionable outside the exercise, resolve the starting-FCFF and WACC gaps.

**Monitor one metric:** next quarter's year-over-year LTM Fee Related Earnings growth, using the comparable figure in KKR's next earnings supplement. If it drops below 15%, revisit the growth path and rerun the valuation rather than retaining the same initiation threshold. FRE growth is an operating indicator, not a substitute for reconciling FCFF.

## GitHub checkout

Upload the two files in this dated folder together: `KKR_reverse_DCF.md` and `dcf.py`. Keep them in the same folder so the code link works. Submit the actual GitHub file URLs after uploading; no remote URL or successful upload is claimed here. The source links, inputs, results, grid, reverse shift, reasonableness test, conditional call and disclaimer are all contained in this document.

---

**Disclaimer:** I am a student, not a financial professional. This document was prepared for FIN 43900 (AI Finance Applications, Purdue) as a class learning exercise. It is not professional investment research or financial advice. I used OpenAI Codex to help with research, analysis, calculations, and drafting. Any remaining errors are my own.
