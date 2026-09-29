# Lab 11 — KKR pro-forma sensitivity

Bernat Pascuet Cuesta · FIN 43900, AI Finance Applications · September 29, 2026

**Over the tested ranges, fee growth has the larger effect on both FY2030 operating profit and common FCFE.** All six scenarios pass the accounting and liquidity checks, and the restored base exactly matches the original. Value per share is unavailable because the Lab 10 valuation remains unresolved.

The sensitivity analysis, prediction reconciliation and post-run partner exchange are documented below. I personally inspected my partner's actual Accenture files. The arithmetic below was also checked against the supplied figures. The partner's model execution checks are reported by them; no separate assistant execution of their model is claimed.

## D — my question

Which assumptions drive KKR's forecast and value, and what explains their effects?

I continued my existing KKR Lab 10 model, using its FY2025 opening balances and FY2026–2030 forecast. I preserved the original model and used an identical copy, [kkr_proforma.py](kkr_proforma.py). The inputs and all five years of base statements exactly match the saved Lab 10 run. [base_snapshot.json](base_snapshot.json) records the inputs, statements and source hash; [lab10_base_output.txt](lab10_base_output.txt) preserves the original terminal output.

## R — my two operating drivers

| Independent input | Lower | Base | Higher | Affected years |
|---|---:|---:|---:|---|
| Annual fees-and-other growth | 5% | 10% | 15% | FY2026–2030, same rate each year |
| AM compensation / AM revenue | 55.116000% | 60.116000% | 65.116000% | FY2026–2030, same ratio each year |

Each endpoint moves **five percentage points** from the base. In code, percentages are decimal fractions: 10% is 0.10. Compensation uses the exact base ratio 4,710.394 / 7,835.508, not its rounded display. Each run changes only one of these assumptions.

**Fee growth:** I use 5%–15% as a judgment range informed by the historical GAAP fees-and-other growth already recorded in Lab 10: 5.0411%, 23.2835% and 11.2292% for FY2023–2025. The low case is close to the slowest observed year; the high case allows an improvement from FY2025 without repeating FY2024's growth. These are scenarios, not guidance or a statistical interval.

**Compensation:** I keep the FY2025-based ratio of 60.116000% and test five points either side. The lower and higher ratios are labelled judgments, not historical minimum and maximum observations. They test how changes in compensation intensity affect the share of AM revenue retained. The ratio applies to both fees-and-other and capital-allocation income.

Historical anchors come from the existing Lab 10 filing work: GAAP fees-and-other of $2,821.627m in FY2022, $2,963.869m in FY2023, $3,653.962m in FY2024 and $4,064.273m in FY2025; FY2025 AM compensation of $4,710.394m and AM revenue of $7,835.508m. Lab 10 cites the FY2023, FY2024 and FY2025 10-K operations tables, printed pp.233, 229 and 163 respectively. No new company data were generated for this lab.

## Outputs and valuation boundary

I use **FY2030 operating profit and signed common FCFE**, both in USD millions, for every run.

Operating profit is the model's consolidated `revenue - expenses`, before net AM investment income. It retains insurance debt interest among insurance expenses, matching Lab 10. It is a consistently defined operating-profit proxy, not standardized EBIT or KKR Fee Related Earnings.

Common FCFE is the model's cash after taxes, capex, outside-investor distributions and assumed insurance retention, before common dividends and revolver financing. All annual signed cash flows are retained.

**Value per share: unavailable.** Lab 10's $10.38 was a provisional scenario. Its historical income fractions do not establish legal ownership of cash or insurance remittance capacity, and the model does not separately schedule future realization of accrued carry. This lab never calls the valuation function or creates a terminal value. The old price and quote remain only in the archived Lab 10 output, not as Lab 11 results.

## My locked prediction

I saved [LOCKED_PREDICTION.md](LOCKED_PREDICTION.md) at **2026-09-29T20:32:38.250152+00:00**, before executing these changed scenarios. The original wording remains unchanged.

For fee growth increasing from **10% to 15% annually**, I expected FY2030 operating profit to rise by roughly **$650m** and common FCFE by roughly **$150m**. My reasoning was that the extra fees compound, compensation absorbs about 60.1%, and taxes, outside investors, working capital and insurance retention reduce the amount available to common shareholders. I expected fee growth to be the larger driver over these ranges. The original record preserves the prediction, its preparation details and prior exposure to Lab 10 sensitivities.

## I — sensitivity results

Final-year outputs and changes are in **USD millions**. Changes equal the changed run minus the original base. All figures below are calculated at full precision and displayed to three decimals.

| Driver | Case | Actual input | Operating profit | Change | Common FCFE | Change | Checks |
|---|---|---:|---:|---:|---:|---:|---|
| Fee growth | Lower | 5.000000% | 2,069.719 | -544.022 | 595.910 | -123.759 | PASS |
| Fee growth | Base | 10.000000% | 2,613.741 | +0.000 | 719.669 | +0.000 | PASS |
| Fee growth | Higher | 15.000000% | 3,265.972 | +652.231 | 867.711 | +148.042 | PASS |
| Compensation / AM revenue | Lower | 55.116000% | 3,185.205 | +571.464 | 822.222 | +102.553 | PASS |
| Compensation / AM revenue | Base | 60.116000% | 2,613.741 | +0.000 | 719.669 | +0.000 | PASS |
| Compensation / AM revenue | Higher | 65.116000% | 2,042.277 | -571.464 | 617.116 | -102.553 | PASS |

| Driver | Operating-profit span | Common-FCFE span | Valid runs |
|---|---:|---:|---:|
| Fee growth | 1,196.253 | 271.801 | 3/3 |
| Compensation / AM revenue | 1,142.928 | 205.106 | 3/3 |

Each span is the maximum minus the minimum across the three valid results. All years have positive FCFE in these scenarios, but the code preserves negative amounts if they occur. [SENSITIVITY_OUTPUT.md](SENSITIVITY_OUTPUT.md) contains six-decimal outputs and per-year checks; [STATEMENT_DETAILS.md](STATEMENT_DETAILS.md) retains the complete statements for every run; [sensitivity_results.json](sensitivity_results.json) stores unrounded results and independent inputs.

The runner starts each scenario with a fresh independent copy of both the base assumptions and opening balances. It reruns the whole linked model and checks that only the selected independent input changed. An invalid run retains the available statements and an error message but is excluded from output spans; incomplete ranges are not ranked against each other.

## V — checks and prediction reconciliation

| Check | Result |
|---|---|
| First base vs saved Lab 10 | PASS: identical assumptions, opening balances and every forecast cell |
| Six scenario runs | PASS: all original accounting links and liquidity checks |
| One input at a time | PASS: only the selected key differs in each lower/higher run |
| Signed differences | PASS: changed output minus unrounded original base |
| Spans | PASS: maximum minus minimum of valid outputs |
| Restored base | PASS: identical inputs and every output cell to the first base |
| Value per share | Unavailable; no valuation routine called |

The original accounting tolerance is **0.000001 USD million ($1)**. Base restoration passes exact equality, which is stricter. The checks include balance-sheet balance, cash-flow and ownership-equity links, income attribution, PP&E, insurance asset backing, FCFE reconciliation, ring-fenced cash, cash floor and revolver capacity. See [VALIDATION.md](VALIDATION.md).

| Locked change: fee growth 10% → 15% | Predicted change | Actual change | Actual minus prediction |
|---|---:|---:|---:|
| FY2030 operating profit, USD millions | +650.000000 | +652.230899 | +2.230899 |
| FY2030 common FCFE, USD millions | +150.000000 | +148.042400 | -1.957600 |

My rough estimate was close because it captured the main revenue and compensation effects. The precise model also includes working-capital needs and insurance investment income from retained capital. These help explain why the profit increase was slightly higher and the cash increase slightly lower than I predicted.

For a traceable result, the higher-fee-growth run adds $1,629.152401m of FY2030 fees and $2.459758m of insurance investment income, while compensation rises by $979.381260m. Their net is the $652.230899m operating-profit increase. Additional tax is $163.057725m and additional working capital is $9.424312m. The resulting cash is allocated to outside investors and common holders, then reduced by common insurance retention, leaving $148.042400m of extra common FCFE. All other independent assumptions remain at base.

## E — what I take from the result

**Over these ranges, fee growth is the larger driver for both outputs.** What stands out is how close compensation comes for operating profit: its ratio applies to capital-allocation income as well as fees, so it affects a broad revenue base. That helps explain why compensation nearly matches the fee-growth profit span even without the same compounding effect.

The cash response is less direct. Reducing compensation by five percentage points raises operating profit by $571.463802m but common FCFE by only $102.552877m. The unpaid-carry-compensation addback also falls by $96.263154m, so part of the accounting saving does not produce the same current cash saving. Taxes, outside-investor allocations and insurance retention further reduce common cash.

I would not treat this ranking as universal. Equal percentage-point widths are not economically equivalent across growth and a cost ratio. Different ranges could change which driver has the largest span, and one-at-a-time runs do not show the combined effect of both assumptions changing together.

This gives me a reason to follow fee-paying AUM, effective fees, fund mix and compensation intensity together. It does not give me a new fair-value estimate. My main unresolved research priority remains the parent cash bridge, including actual insurance distributions and carry realization.

## Reflection and partner review

My first-person prediction reconciliation, reflection and short answers on sensitivity are in [STUDENT_RECORD.md](STUDENT_RECORD.md). The supplied partner questions, KKR input confirmation and recomputation, drafted responses, and reciprocal Accenture arithmetic/bridge check are recorded in [PARTNER_EXCHANGE.md](PARTNER_EXCHANGE.md). I subsequently confirmed that I personally inspected the actual Accenture files. This student inspection is separate from the assistant's arithmetic checks; it is not a claim that the assistant reran their model. I have not reused the Lab 10 partner exchange as evidence of a new discussion or claimed that my partner checked the prediction before the run.

I first developed the prediction and its main idea myself, then used AI to refine it. The saved pre-run timestamp belongs to the refined version; it does not establish a separate timestamp for my earlier original idea. My later clarification and personal inspection confirmation are recorded in [PARTICIPATION_CLARIFICATION.md](PARTICIPATION_CLARIFICATION.md). The documented partner exchange occurred after the runs; no earlier partner review is claimed.

## Run and GitHub checkout

From this folder:

```bash
python3 kkr_sensitivity.py
python3 kkr_sensitivity.py --self-test
python3 kkr_sensitivity.py --run
```

The first command checks the unchanged base; the second tests the sensitivity plumbing on synthetic data; the third reproduces the six configured scenarios and restored base. The code uses only Python's standard library. [sensitivity_inputs.json](sensitivity_inputs.json) contains the exact settings, and [locked_inputs_used.json](locked_inputs_used.json) preserves the configuration frozen before the first changed run. Re-running the same configuration is supported; changed settings require preserving the earlier evidence first.

Upload the report, student record, locked prediction, both Python files, JSON inputs/results and Markdown evidence together. The main links are `Lab11_KKR.md` and `kkr_sensitivity.py`; the latter also needs `kkr_proforma.py`, `base_snapshot.json` and `sensitivity_inputs.json`. Visible output is included so the reader does not need to execute the code. Bernat handles GitHub; no upload or submission is claimed here.

## Disclaimer

I am a student, not a financial professional. This document was prepared for FIN 43900 (AI Finance Applications, Purdue) as a class learning exercise. It is not professional investment research or financial advice. I used OpenAI Codex to help with research, analysis, calculations, and drafting. Any remaining errors are my own.
