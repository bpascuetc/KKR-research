# Lab 10 — KKR: filings, five-year pro forma and common-share value

Bernat Pascuet Cuesta · FIN 43900, AI Finance Applications · September 24, 2026  
Company: **KKR & Co. Inc. (NYSE: KKR)** · USD millions except per-share amounts

## Result and scope

**The simplified scenario produces $10.38 per as-converted common share.** All five forecast balance sheets balance, corporate cash remains above the $1,000 million floor, and the model rejects deliberately broken statements. This is a **provisional classroom scenario, not a defensible stand-alone estimate of KKR's fair value**: consolidated cash cannot be reliably allocated to parent shareholders using a single historical income percentage. The large difference from both today's market quote and the prior $68.92 DCF is a reason to challenge the cash-allocation assumptions, not a recommendation.

The research, runnable model, history, ratios, assumption explanations and automated checks are prepared. The supplied KKR and Accenture partner challenges, written responses and first-person reflection are recorded below. **Both requested figures have been verified directly against the filing, and Bernat confirmed personally inspecting both pages and finding the figures correct. GitHub submission remains pending.** No completed oral discussion is claimed.

## D — the question and the company-specific line

**What are five years of KKR's statements worth, built from assumptions that can be defended?**

Suggested explanation to a partner: “KKR has insurance policy liabilities and investment-fund investors, so money entering the consolidated group is not automatically cash available to KKR common shareholders; I must model insurance asset backing, unrealized income and outside investors separately.”

There is **no dealer floor-plan row**. The replacement is **insurance policyholder deposits and credited interest, matched by investment purchases**, plus a separately disclosed allowance for retained insurance capital. New deposits increase both investments and policy obligations, not shareholder income. Investments are not relabeled inventory; fees are not assigned an invented retailer gross margin.

The existing [Lab 09 ABG model, reference copy](sources/ABG_proforma_reference.py) was rerun: its self-test reproduces the $291.75 answer and rejects the -$61.4 million cash break. Its original remains in `Lab09/2026-09-22/proforma.py`. KKR is saved in a new file, [kkr_proforma.py](kkr_proforma.py), preserving the ABG exercise.

## R — three years of filing history

Sources are the three latest annual filings available for this exercise: [FY2023 10-K](sources/KKR_2023_10-K.pdf), [FY2024 10-K](sources/KKR_2024_10-K.pdf), and [FY2025 10-K](sources/KKR_2025_10-K.pdf). Original company links and file hashes are in [source_index.json](sources/source_index.json). The 2025 file was already in the course folder; the older two were retrieved from KKR's investor-relations document library. Page references below are one-based PDF/printed pages, not zero-based indices. Filings state dollars in thousands; the table divides by 1,000.

| Requested history / exact mapping | FY2023 | FY2024 | FY2025 | Filing locator for 2023 / 2024 / 2025 |
|---|---:|---:|---:|---|
| Reported total revenue | 14,499.312 | 21,878.698 | 19,464.307 | Each year's 10-K, operations, pp.233 / 229 / 163 |
| Gross profit | N/A | N/A | N/A | Same statements: no consolidated COGS/gross-profit subtotal |
| SG&A | Not separately reported | Not separately reported | Not separately reported | Same statements: no single equivalent SG&A line |
| AM/Strategic Holdings general, administrative and other | 1,056.899 | 1,311.676 | 1,479.796 | Operations, pp.233 / 229 / 163; partial SG&A mapping only |
| Insurance general, administrative and other | 746.215 | 745.096 | 756.019 | Operations, same pages; excludes separately reported insurance expenses |
| Consolidated net income | 5,357.086 | 4,906.037 | 6,145.412 | Operations, pp.234 / 230 / 164 |
| Net income attributable to KKR, before preferred dividends | 3,732.261 | 3,076.245 | 2,370.463 | Operations, pp.234 / 230 / 164 |
| Net income attributable to common stockholders | 3,680.514 | 3,076.245 | 2,251.867 | Operations, pp.234 / 230 / 164 |
| Dealer inventory | N/A | N/A | N/A | Financial condition, pp.229–230 / 225–226 / 159–160; no separate inventory row |
| Net fixed assets: disclosed AM/Strategic Holdings PP&E proxy | 863.096 | 902.896 | 975.498 | Other Assets note, pp.327 / 319 / 250 |
| KKR stockholders' equity, including preferred, excluding outside NCI | 22,858.694 | 23,651.568 | 30,902.561 | Financial condition, pp.230 / 226 / 160 |

**N/A is not zero.** Group-wide PP&E distinct from the disclosed AM fixed assets is not separately established here; the model freezes the residual other-asset balance rather than inventing an insurance PP&E number. AM fixed-asset depreciation is isolated from its G&A to avoid charging it twice. Stockholders' equity is not total consolidated equity: FY2025 total equity also includes $48,019.108 million of outside noncontrolling interests, while $2,710.242 million of redeemable NCI is presented separately.

The provider's $25.65 billion revenue figure is not substituted for the filing's $19.464 billion total-revenue row. KKR presents AM investment income separately below operating expenses; mixing the two definitions would corrupt the revenue-growth and margin calculations. Provider data are used only as the explicitly requested capex cross-check and market quote.

[history.csv](history.csv) records a filing locator for each observation. [FILING_REVIEW_PAGES.pdf](sources/FILING_REVIEW_PAGES.pdf) collects the relevant pages. **Two suggested personal checks:** FY2025 total revenue **19,464,307 thousand** on filing p.163; FY2025 net fixed assets **975,498 thousand** on p.250. Both were rechecked directly against the original PDF on September 24 and match the model/report. See [completed source-check record](FILING_CHECKS.md) and [the two original pages](sources/TWO_FILING_CHECKS.pdf). Bernat subsequently confirmed that he personally inspected both pages and found the figures correct.

### Ratios and cash spending

| Ratio / input | FY2023 | FY2024 | FY2025 | Definition and source |
|---|---:|---:|---:|---|
| Gross margin | N/A | N/A | N/A | No reported compatible gross-profit subtotal |
| SG&A / gross profit | N/A | N/A | N/A | No compatible numerator/denominator; not forced to 100% |
| Inventory days | N/A | N/A | N/A | No retailer inventory/COGS combination |
| AM fixed-asset D&A | 68.400 | 71.600 | 81.400 | Other Assets note, pp.327 / 319 / 250 |
| Opening net fixed assets | 857.903 | 863.096 | 902.896 | Same notes, prior-year columns |
| D&A / opening net fixed assets | 7.9729% | 8.2957% | 9.0154% | Matching AM scope, opening denominator as in ABG |
| Fixed-asset purchases in filing, outflow magnitude | 108.393 | 141.536 | 160.765 | Cash flows, pp.239 / 235 / 169 |
| Provider capex field, signed cash outflow | -108.39 | -141.54 | -160.77 | [Stock Analysis annual cash flows](https://stockanalysis.com/stocks/kkr/financials/cash-flow-statement/), FY columns, accessed Sept.24 |
| Tax expense / consolidated pretax income | 18.2699% | 16.2854% | 13.4347% | 1,197.523/6,554.609; 954.396/5,860.433; 953.748/7,099.160; operations pages above |
| Reported total-revenue growth | 154.1875% | 50.8947% | -11.0354% | Year / previous year minus 1; FY2022 revenue 5,704.180 from FY2023 filing p.233 |
| GAAP fees-and-other growth | 5.0411% | 23.2835% | 11.2292% | 2,963.869/2,821.627; 3,653.962/2,963.869; 4,064.273/3,653.962, minus 1 |
| Segment management-fee growth, supplemental | 14.0726% | 14.2247% | 18.4741% | Segment notes pp.358 / 349 / 280; 3,030.325, 3,461.381, 4,100.841; FY2022 2,656.487 |
| Comparable group-wide organic / same-store growth | Unresolved | Unresolved | Unresolved | No comparable percentage identified in reviewed MD&A; fee growth is not relabeled organic |

Provider capex agrees with the filing at its two-decimal display precision. Its broader D&A field is **not** used with AM-only PP&E. The three-year effective consolidated tax rate includes income allocated to noncontrolling investors, so it is not automatically the marginal tax rate on KKR's own earnings. See [ratios.csv](ratios.csv) for unrounded calculations.

### Organic growth: explanation for the discussion

Organic growth measures expansion of the existing business after excluding effects such as acquisitions; the exact currency, disposal and perimeter adjustments depend on the issuer's definition. Same-store sales are the retail version, measured on a comparable set of locations. The provided ABG exercise uses 1.8% for the existing-business forecast rather than extrapolating 4.7% reported growth, which can include changes in the business perimeter; the underlying video's exact 2.9-point reconciliation was not supplied and is not fabricated here.

For KKR, examine fundraising, distributions/redemptions, changes in fee base, investment values, and acquisitions in the AUM/FPAUM rollforwards. FY2025 Private Equity FPAUM, for example, separately reports **$3,214 million from acquisitions** (FY2025 10-K p.108). A growth rate that includes this amount is not purely organic. Segment management fees also include intersegment fees, whereas consolidated GAAP fees reflect consolidation eliminations. Neither series is a substitute for an undisclosed same-perimeter metric.

## Opening balance sheet and model boundaries

| FY2025 opening line | USD millions | Source / reconciliation |
|---|---:|---|
| Corporate cash | 4,562.361 | FY2025 p.126: 9,380.874 - 4,818.513; excludes 227.292 short-term investments |
| Other consolidated cash, treated as unavailable to parent | 12,329.786 | AM cash + insurance cash on p.159, less corporate cash above |
| Restricted cash | 259.643 | 48.033 AM + 211.610 insurance, p.159 |
| AM/Strategic Holdings investments | 127,948.305 | p.159; includes consolidated funds, not wholly owned parent assets |
| Insurance investments | 192,009.748 | p.159 |
| AM fixed assets, net | 975.498 | p.250; carved out of other assets, not added twice |
| Insurance intangible assets | 5,905.228 | p.159 |
| Other assets | 66,153.503 | p.159: 2,307.701 due from affiliates + (6,294.381 - 975.498) AM other assets + 48,022.605 reinsurance recoverable + 6,662.911 insurance other assets + 3,841.403 separate accounts |
| **Total assets** | **410,144.072** | Agrees to p.159 |
| AM/Strategic Holdings debt | 49,117.744 | p.159; includes fund/CFE debt |
| Insurance debt | 3,820.407 | p.159 |
| Insurance policy liabilities | 205,558.727 | p.159 |
| Other liabilities | 70,015.283 | p.159: 442.362 + 14,348.335 + 46,822.744 + 3,341.695 + 1,218.744 + 3,841.403 |
| **Total liabilities** | **328,512.161** | Agrees to p.159 |
| Redeemable NCI, mezzanine claim | 2,710.242 | p.160 |
| KKR stockholders' equity | 30,902.561 | p.160; includes 2,543.404 preferred stock |
| Outside NCI equity | 48,019.108 | p.160 |
| **Assets - liabilities - equity - redeemable NCI** | **0.000** | Independently recomputed by code |

The balance sheet starts from audited **December 31, 2025**, as requested for the three-10-K exercise. The saved June 2026 DCF inputs are useful background but are not mixed into this opening balance sheet. Thus FY2026 is a full-year scenario, not actual year-to-date results plus a quarterly forecast. Cash at the September 24 valuation date is estimated by uniform interpolation; this limitation is material.

## Labelled assumption set

The three columns below contain the assumption name with its value, the label, and its reason. **Every forecast extension of a historical observation is a judgment.** No unsupported item is labelled company guidance.

| Value / model line | Label | Reason and what would change it |
|---|---|---|
| Opening balance sheet and FY2025 operating lines above | History | Start from one internally consistent audited date; change only after a reconciled later-period bridge. |
| AM fees-and-other growth: 10% annually | Judgment | Below the observed FY2025 11.23% GAAP growth and segment fee growth; lower it if fundraising, realizations or fee-paying assets weaken. Neither series proves organic growth. |
| Capital-allocation income growth: 5% | Judgment | Use slower growth than fees because carry and investment performance are cyclical; change with fund-level realization and valuation evidence. |
| Insurance premiums, fees, other income and specified expenses: 5% | Judgment | Modest common volume path avoids extrapolating one-off reinsurance-driven revenue jumps; replace with a product/block forecast when available. |
| AM compensation / AM revenue: 60.1160% | Judgment, FY2025 history anchor | 4,710.394/7,835.508; holds compensation intensity constant, including performance compensation; change if mix or the compensation framework changes. |
| Occupancy and AM G&A excluding fixed-asset D&A: 5% growth | Judgment | Slower than fee growth allows limited operating leverage; change with headcount/occupancy or compliance costs. |
| Fixed-asset D&A / opening fixed assets: 9.0154% | Judgment, history anchor | 81.4/902.896; matches scope and an opening denominator; change with asset lives or investment mix. |
| Capex: 160.765 in FY2026, +5% annually | Judgment, history anchor | FY2025 fixed-asset purchases provide a transparent starting budget; growth allows maintenance/expansion without borrowing ABG's $250m. |
| AM investment total gain yield: 3% of opening investments | Judgment | A modest positive mark/realization scenario, not a guaranteed return; negative return scenarios remain possible. |
| Cash-realized fraction of AM gains: 25% | Judgment | Recognize that fair-value gains are not all cash; 2025 realized net gains were only 202.864 of 4,801.453 total (p.169), so 25% already assumes a recovery in realization. Change using asset-level exits. |
| Cash-realized fraction of current capital-allocation income: 60% | Judgment | Separates cash carry from accruals; future recovery of the remaining 40% is not separately scheduled, a conservative limitation that requires a carry-vintage rollforward to fix. |
| Unpaid carry compensation: compensation ratio × uncollected capital income | Judgment | Match part of performance compensation timing to accrued income; change using actual compensation liabilities and payout terms. |
| AM dividend yield: 1.229336%; interest yield: 2.714891% | Judgment, history anchors | FY2025 dividends 1,440.790 and interest 3,181.871 divided by average 2024/2025 AM investments; apply to opening forecast investments to avoid circularity. |
| Insurance investment yield: 4.233059% | Judgment, history anchor | 7,665.106 / average(170,144.744, 192,009.748); revise for reinvestment rates, credit losses and asset mix. |
| AM debt rate: 5.843024%; insurance debt rate: 7.830610% | Judgment, history anchors | FY2025 interest / average matching 2024–2025 debt balances; these are aggregate accounting yields, not marginal borrowing quotes. |
| Policy interest-credit proxy: 2.694419% of opening policy liabilities | Judgment, history anchor | 4,990.209/185,205.366 from p.169/p.159; uses a broad policy-liability denominator rather than an actuarial credited-rate estimate. |
| Net deposit proxy: 3.792484% of opening policy liabilities | Judgment, history anchor | (28,507.218 - 21,483.334)/185,205.366 from pp.170/159; invest deposits dollar-for-dollar and do not call them earnings. |
| Insurance cash-claim proxy: 5,740.944 in opening year, +5% | Judgment, history anchor | 10,731.153 policy expense less 4,990.209 credited-interest adjustment; a coarse residual, not reported cash claims or an actuarial reconciliation. |
| Policy acquisition spending: 1,062.606 opening run rate; amortization: 309.319; both +5% | Judgment, history anchors | pp.169/163; cash spending increases intangibles and amortization reduces them. Actual product economics may differ materially. |
| Future insurance fair-value gains/losses and OCI: zero | Judgment | Avoid forecasting ungrounded rate/derivative marks; this removes FY2025 insurance losses, so it is not uniformly conservative. |
| Cash tax: 25% of positive consolidated pretax income; no loss benefit | Judgment | Uses the prior class tax scenario and avoids treating the low consolidated effective rate as a permanent parent tax rate. A legal-entity tax forecast could differ substantially. |
| Incremental other working capital: 2% of fee-revenue increase | Judgment | Allow some collection-related capital needs; revise with receivable/payable rollforwards. |
| Outside NCI share of income and positive cash pool: 58.903227%; redeemable NCI: 2.523883% | Judgment, history anchors | 3,619.846/6,145.412 and 155.103/6,145.412. These are FY2025 income fractions, **not legal ownership percentages**; fixed allocations are the largest unresolved economic weakness. |
| KKR residual income share: 38.572890% | Judgment, derived | Remainder after the two outside-income fractions; excludes a second allocation of outside investor value to common shareholders. |
| Retain 20% of positive common cash capacity in insurance investments | Judgment | Explicit allowance for capital support; this is **not** a verified regulatory-capital requirement or proof that the other 80% is distributable. Replace with legal-entity remittance and capital budgets. |
| Corporate cash floor: 1,000 | Judgment | Preserves the prior KKR exercise's operating reserve and keeps fund/insurance cash unavailable for the parent check; revise with commitments and liquidity needs. |
| Model revolver limit: 1,000; opening draw: zero; rate: 6% | Judgment / history for zero reported AM revolvers | Scenario borrowing allowance, not a claim that a $1bn unrestricted line is committed. The filing p.253 has larger aggregate facilities with different borrowers and restrictions. Baseline needs no draw. |
| Existing debt unchanged; maturities refinanced at carrying amount; no net new term debt | Judgment | Isolate operating assumptions; no refinancing fee or changed rate is assumed. Add maturity-specific refinancing when supported. |
| Future buybacks, new outside capital, M&A and other structural balance movements: zero | Judgment | Avoid inventing transaction terms. Actual 2026 transactions are not forecast; this is not a comprehensive current-event model. |
| Other cash and restricted cash frozen; residual assets/liabilities frozen except explicit links | Judgment | Prevent inaccessible balances becoming a cash plug. Claims, working capital and investment links change only through stated schedules. |
| Equity compensation treated as cash-settled compensation; no future incremental share issuance | Judgment | Keeps its economic cost in expenses and avoids claiming free noncash addbacks; actual dilution or cash costs may differ. Carry-compensation timing is separately modelled. |
| Shares: 891.451844 + 20.8 = 912.251844 million, fixed | Judgment using history / disclosed conversion illustration | FY2025 common shares p.160 plus p.126's illustrative Series D conversion shares. Assumes immediate conversion before forecast, eliminating future preferred dividends and principal deductions. Actual conversion is price-dependent; exchangeable NCI remains outside, and other potential dilution is not fully modelled. |
| Common dividend: $0.78/share/year | Judgment, prior June 2026 evidence | Holds the saved annualized common payout constant; no additional assumed buybacks. Dividends are financing after FCFE, not an operating expense. |
| Cost of equity: 4% + 1.7930 × 5% = 12.965% | Judgment plus historical beta estimate | Beta comes from the saved Sept.22 regression; 4% risk-free rate and 5% ERP are explicit scenarios, **not today's sourced market inputs**. Use cost of equity because cash flows are after interest. |
| Terminal FCFE growth: 3%; cost of equity must exceed growth | Judgment | Lower than explicit fee growth; requires the final cash-conversion/capital-retention economics to remain sustainable, which is unverified. |
| Valuation timing: 98/365 of FY2026 FCFE, then four full years | Judgment | Uniform-accrual approximation from Sept.24 to Dec.31; excludes already elapsed annual cash flow. Interim reported cash flows would improve this. |

**My explanation of the 60% cash-realization judgment:** I use 60% because recognizing carry in earnings does not mean KKR can distribute it immediately, and the model should show the uncollected part in investments rather than cash. I would change it after reconciling beginning carry, new accruals, reversals and cash distributions by fund; until then, the 40%–80% sensitivity is more informative than claiming 60% is measured history.

## I — statement links and personalization

Revenue and expense schedules determine pretax income; cash tax gives consolidated net income; outside-income allocations determine KKR's share. The as-converted convention changes the composition of parent equity but not total opening equity. Fixed-asset depreciation is already excluded from starting cash G&A, and the expense is separately recomputed on opening PP&E.

The cash-flow statement reverses unrealized gains and uncollected carry, adds unpaid associated compensation, depreciation, policy amortization and credited interest, and deducts incremental working capital and policy acquisition spending. Policy acquisition spending is an **operating** outflow, matching the filing; fixed-asset purchases and insurance investment purchases are investing outflows.

Policyholder deposits are financing cash inflows. Investments increase by deposits plus credited interest plus retained common capital; policy liabilities increase by deposits plus credited interest. Therefore deposits and credited interest do **not** create immediate common FCFE. Accrued carry and unrealized gains increase AM investments; unpaid carry compensation increases other liabilities. Each ownership class's equity rolls by its earnings minus its distributions.

Common FCFE equals operating cash flow plus investing cash flow plus net policy deposits, less the two outside-investor distributions. It is **before common dividends and revolver changes**, and after insurance reinvestment. All positive consolidated cash capacity is allocated using the disclosed historical-income fractions; when the pool is negative, outside cash distributions stop and the corporate liquidity scenario bears the residual funding need. That downside allocation is a simplification, not a statement about contractual obligations.

Cash is the **result** of cash flows and financing. The code never solves cash as assets minus liabilities minus equity. A separate recomputed balance check and cash-flow-link check guard valuation. New revolver borrowing is limited, charged interest next year and repaid from subsequent surplus before cash accumulates. No separate Global Atlantic value or principal-investment book value is added to a model already containing their income and assets.

## V — five years, checks and the price

The complete income statements, balance sheets and cash-flow statements are in [PROJECTED_STATEMENTS.md](PROJECTED_STATEMENTS.md), with unrounded values in [projected_statements.csv](projected_statements.csv) and [model_results.json](model_results.json).

| USD millions | FY2026E | FY2027E | FY2028E | FY2029E | FY2030E |
|---|---:|---:|---:|---:|---:|
| Total revenue | 21,813.383 | 23,289.588 | 24,870.963 | 26,565.575 | 28,382.153 |
| Consolidated net income | 5,589.401 | 6,011.927 | 6,462.896 | 6,944.500 | 7,459.124 |
| KKR as-converted common net income | 2,155.993 | 2,318.974 | 2,492.926 | 2,678.694 | 2,877.200 |
| Common FCFE | 372.440 | 449.182 | 532.249 | 622.206 | 719.669 |
| Corporate cash | 4,223.244 | 3,960.870 | 3,781.563 | 3,692.212 | 3,700.325 |
| Cash headroom above $1,000m floor | 3,223.244 | 2,960.870 | 2,781.563 | 2,692.212 | 2,700.325 |
| Revolver | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| Assets - liabilities - equity - redeemable NCI | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

No baseline year draws the revolver: the opening corporate buffer covers common distributions exceeding FCFE in the first four years. The $12,329.786 million of other cash does not fund that buffer. All five years have positive FCFE.

The deliberate test deducts $100 million from FY2026 cash and refuses **before** valuation:

```text
MODEL REFUSED: FY2026 assets - liabilities - equity - redeemable NCI gap -100.000000
```

Tests also check a coordinated cash/equity corruption that still balances but breaks the cash-flow link; revolver borrowing and next-year interest; insufficient borrowing capacity; lower carry realization; and negative-FCFE handling. The model retains negative FCFE in the statements. Per the lab, its positive-only valuation omits explicit deficits and withholds a terminal value when final FCFE is nonpositive; it also prints a signed-cash-flow diagnostic so omitted funding needs stay visible. A negative final cash flow does not support a **positive going-concern perpetuity value** without a recovery or funding model, although the algebra itself can produce a negative number.

### Valuation bridge

| Component, September 24 timing | USD millions |
|---|---:|
| PV of remaining FY2026 and FY2027–2030 common FCFE | 1,730.684 |
| PV of terminal common FCFE | 4,420.812 |
| Estimated excess corporate cash, less estimated revolver | 3,314.295 |
| **As-converted common equity scenario value** | **9,465.791** |
| As-converted shares, millions | 912.251844 |
| **Value per share** | **$10.38** |

Terminal value is FY2030 FCFE × 1.03 / (0.12965 - 0.03), discounted 4 + 98/365 years. Corporate cash at the valuation date is approximated at $4,314.295 million using the FY2026 cash path; subtract the $1,000 million floor. Future cash already represented by FCFE is not added again. Fund/insurance cash and restricted cash are not added. Existing term debt is already reflected in after-interest cash flows and the refinancing assumption, so it is not deducted again. Terminal value supplies 46.70% of total value, or 71.87% of the discounted future-cash-flow component excluding excess cash.

**The model says $10.38 per share and the market provider's September 24, 2026, 4:00 p.m. EDT header says $95.64; using the same assumed 912.251844 million as-converted shares for both, what stronger evidence about cash realization, outside-investor allocations and insurance distributions would explain the difference?** No investment recommendation is made.

Quote source: [Stock Analysis KKR history](https://stockanalysis.com/stocks/kkr/history/), accessed September 24. Its header displayed $95.64 at 4:00 p.m., while the September 24 table row displayed $95.49; the independent closing-price reconciliation is **unresolved**. The earlier 3:27 p.m. overview snapshot was $95.28. This report selects the timestamped closing header transparently; the $0.15 disagreement is much smaller than model uncertainty. Multiplying the selected quote by the model denominator is a like-denominator scenario comparison, **not** a claim about reported current market capitalization or actual current diluted shares.

### Why the answer is so different from our previous DCF

The September 10 $68.92 result valued an adjusted asset-management FCFF proxy at 11% WACC and added separate insurance/holdings values. This exercise starts from consolidated GAAP balances, subtracts policy acquisition spending and unrealized income, allocates cash to outside investors using a coarse proxy, retains insurance capital, uses 12.965% cost of equity, and applies a different disclosed dilution convention. It is not an update using the same economic definition, and the two prices must not be averaged.

The new model's low payout capacity is **not source-verified parent FCFE**. In particular, GAAP income fractions need not match legal ownership, cash allocations or insurance remittance capacity; uncollected carry is not given a future realization schedule. Consequently, $10.38 is useful as the output of an auditable scenario but not as evidence that the market price is wrong. A parent-level, segment-by-segment cash bridge is the highest-priority improvement.

| One-at-a-time change; all other assumptions fixed | Value/share |
|---|---:|
| Base | $10.38 |
| Current capital income realized in cash: 40% | $9.39 |
| Current capital income realized in cash: 80% | $11.36 |
| No extra common capital retention | $12.09 |
| All AM investment gains realized in cash | $19.66 |
| Cost of equity 10% | $13.40 |
| Cost of equity 15% | $9.17 |

These are scenario diagnostics, not a confidence interval. Even generous realization in this model does not bridge the market gap, reinforcing the need to investigate model scope and ownership cash allocation rather than calibrate a growth rate to the quote.

## E — partner review and my reflection

### My partner's challenge to KKR

> Your revenue growth assumption is applied to a revenue line that is not a steady business: KKR's GAAP revenues went from $14,499M in 2023 to $21,879M in 2024 (+51%) and back to $19,464M in 2025 (−11%), and the 2024 jump came largely from net premiums of $7,899M, which the 10-K ties to one large block reinsurance transaction at Global Atlantic. Why that number, when a single growth rate on total revenue carries one-off reinsurance deals and investment gains forward as if they recur — and what would change it: would you get a different value if you grew fee-paying AUM or management fees instead?

**My answer — two sentences:** I chose 10% for the asset-management fees-and-other line, not total GAAP revenue, because it is below the latest 11.23% growth in that line and 18.47% growth in segment management fees; the model forecasts insurance and investment income separately from a 2025 base, although I accept that its 5% insurance-premium growth still needs a recurring-versus-one-off breakdown. Applying the historical 18.47% management-fee growth rate to the existing fee line raises the scenario value from $10.38 to $12.68 with everything else held fixed, so I would revise the judgment using average fee-paying AUM, effective fee rates and fund-mix evidence, while modelling block reinsurance deals separately rather than extrapolating reported total revenue.

**What the sensitivity establishes:** This is a change to `fee_growth` in the current model, not a completed FPAUM-driven replacement. The existing fees-and-other line includes more than management fees, and consolidated fees differ from segment fees because of eliminations. A proper replacement would forecast management fees as average fee-paying AUM × an appropriate fee rate by strategy, forecast transaction/other fees separately, and reconcile consolidation eliminations. Changing growth drivers does not automatically make the valuation reliable while ownership cash allocation and insurance remittances remain unresolved.

| Fee-line sensitivity, all other assumptions fixed | Growth | Value/share |
|---|---:|---:|
| Flat fees-and-other | 0% | $8.37 |
| Base judgment | 10% | $10.38 |
| FY2025 FPAUM growth used only as a fee-line growth proxy | 18.0054% | $12.54 |
| FY2025 segment management-fee growth used as a fee-line growth proxy | 18.4741% | $12.68 |

FPAUM growth is calculated as 604,144/511,963 - 1 (FY2025 10-K, MD&A); management-fee growth is 4,100.841/3,461.381 - 1 (p.280). These historical growth rates are sensitivity inputs, not management guidance. The base-case assumption and valuation remain unchanged.

### My challenge to my partner — Accenture

**Judgment challenged:** Business optimization costs = zero in FY2027E–FY2030E.

> You call business optimization a one-time cost and set it to zero after FY2026, but Accenture has booked it four years running — $1,063M in FY23, $438M in FY24, $615M in FY25 and $308M in FY26. That is closer to a recurring cost of about $600M a year. Why is zero the right number, and how much of your $182 comes from assuming it stops?

**My partner's supplied answer:**

> I set it to zero because management says the program that began in Q4 FY25 was completed in Q1 FY26 and no new program has been announced, and I would rather not invent a charge the company has not disclosed.
>
> If it keeps recurring at the four-year average of about $600M a year, my value falls by about $8.55 a share, to roughly $173 — below the market price — so a new program announced with the FY26 results on Oct. 1 would change this label from judgment to guidance and flip the model-versus-market comparison.

**My assessment:** Completing one named program does not rule out future optimization programs, so zero remains a judgment about future spending rather than evidence that the cost category disappears. The reported sensitivity answers how much that judgment matters; an announcement would become guidance only to the extent that management specifies costs and timing, while later-year extrapolations would remain judgments.

The Accenture figures, announcement timing, valuation and $8.55 sensitivity above are supplied from the partner's work; their filings and model have not been independently recalculated here. The arithmetic average of the four supplied charges is $606 million, and $182 - $8.55 = $173.45, consistent with the rounded wording.

### My reflection and judgment explanations

I would defend the 10% fee-growth judgment longest because it focuses on the fee-generating business and is below both the latest growth in consolidated fees-and-other and segment management fees. I would lower it if fundraising or fee-paying AUM weakened, fee rates fell, or more funds moved to a lower post-investment-period fee base; I would raise it only with evidence of sustained growth in the fees KKR can actually retain.

I use 60% cash realization for capital-allocation income because accounting income is not automatically cash available to shareholders. I would replace that assumption with a rollforward of accrued carry, realizations and reversals when I can trace the amounts, rather than assume all accrued gains will be collected immediately.

The 20% insurance-capital retention assumption is the judgment I am least confident about: it creates an explicit reinvestment deduction, but it does not establish how much Global Atlantic can legally distribute. I would change it using its capital requirements, growth plans and permitted distributions, and I would also replace the historical consolidated-income split with a parent-level cash bridge.

The number that surprised me was the difference between KKR's $410.144 billion of consolidated assets and $30.903 billion of KKR stockholders' equity in 2025. It explains why I cannot treat all of the group's assets, cash or earnings as belonging to KKR common shareholders, and why a balanced model can still have an uncertain valuation.

### Participation record

| Required activity | Status |
|---|---|
| KKR-specific explanation | Written explanation supplied; oral discussion not independently confirmed |
| Filing figure 1: FY2025 revenue, p.163 | PASS: $19,464.307m; Bernat confirmed personal inspection |
| Filing figure 2: FY2025 net fixed assets, p.250 | PASS: $975.498m; Bernat confirmed personal inspection |
| Judgment explanations and reflection | Written above |
| Partner challenge to KKR | Supplied and recorded verbatim above |
| Written two-sentence response | Added above with recalculated fee-growth sensitivity |
| Challenge to Accenture and partner's response | Supplied and recorded above |
| Organic-growth discussion | Written explanation supplied; oral discussion not claimed |

Both personal filing checks are confirmed by Bernat separately from the partner-review record. The economic cash-allocation limitation remains unresolved.

## Run and GitHub checkout

From this dated Lab 10 folder:

```bash
python3 kkr_proforma.py
python3 kkr_proforma.py --self-test
python3 kkr_proforma.py --break-cash
python3 kkr_proforma.py --export
```

The break command is expected to exit unsuccessfully; it changes no saved input. Running normally again restores the valid scenario. The model uses only the standard library. `--export` regenerates statement Markdown, CSV and JSON; the report's narrative and summary tables should be refreshed if assumptions change. The separate `build_evidence.py` recreates evidence CSVs and PDF extracts; it requires `pypdf`, which is not needed to run the financial model.

Upload the files in the prepared submission ZIP together, preserving paths. The main submission links should be **Lab10_KKR.md** and **kkr_proforma.py**, with the linked statement/evidence files alongside them. Do not upload `.tools` or `__pycache__`. There is no configured Git repository/remote or supplied destination URL in this course folder, and browser discovery returned no available connection, so **no GitHub upload or submission is claimed**. Actual GitHub file URLs remain pending the repository destination and authenticated access.

Next week's starting point is this unchanged base case. Before each new assumption experiment, record the predicted direction of the value/cash effect, then run and compare; do not retroactively describe an observed result as a locked prediction.

## Disclaimer

I am a student, not a financial professional. This document was prepared for FIN 43900 (AI Finance Applications, Purdue) as a class learning exercise. It is not professional investment research or financial advice. I used OpenAI Codex to help with research, analysis, calculations, and drafting. Any remaining errors are my own.
