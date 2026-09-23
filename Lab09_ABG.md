# Lab 09 — ABG three-statement pro-forma and validation

Bernat Pascuet Cuesta · FIN 43900 · September 22, 2026

## Question and result

What are five years of a company's statements worth, built from assumptions you can defend, and how do you know the statements are right?

Using the instructor's ABG training assumptions, the model produces equity value of **$5,237.34 million**, or **$291.75 per share**. The present value after 2030 is **$4,177.46 million**, representing **79.76%** of total value. The five explicit FCFE have present value **$1,059.87 million**. Independently rounded components can differ from the rounded total by $0.01 million.

The model reproduces the supplied answer and rejects a deliberately broken balance sheet before valuation. This establishes implementation consistency with the assignment; it does not establish that the assumptions predict actual ABG results.

## Files and execution

The standalone [proforma.py](proforma.py) uses only Python's standard library. Its opening balances and assumptions are editable at the top. All dollar amounts and shares are in millions except value per share. It retains unrounded calculations and the exact three historical ratios from the supplied instructions.

From the course folder:

```bash
python3 proforma.py
python3 proforma.py --self-test
python3 proforma.py --break-cash
```

The last command intentionally exits unsuccessfully, before printing a valuation. Run the first command again for the unchanged, correct model; the demonstration does not edit the saved inputs.

The prior Week 3 KKR model was also rerun with `python3 dcf.py --kkr`: it reproduces $68.9167 per share and its sensitivity grid. The flag is needed because that saved file defaults to a separate classroom training case.

## Method and assumptions

The supplied September 22 lab text and screenshots are the source for this historical training case. No live prices, updated filings, or replacement inputs were introduced. The labels below follow the instructor's table, not independent source verification.

| Input | Value | Instructor label |
|---|---|---|
| Revenue growth | 1.8% annually | Judgment |
| Gross margin | 17.05% | Judgment |
| SG&A / gross profit | 66.5%, 65.5%, 64.5%, 64.5%, 64.5% | Judgment |
| Depreciation / opening PP&E | 82.4 / 3,070.4 | History |
| Annual impairment | 120 | Judgment |
| Annual capex | 250 | Guidance |
| Tax rate | 25.5%; no tax benefit on losses | Judgment |
| Inventory days | 2,135.8 / (17,999.0 − 3,071.7) × 365 | History |
| Floor plan / inventory | 2,027.0 / 2,135.8 | History |
| Other working-capital increase | 0.8% × revenue increase | Judgment |
| Minimum cash / revolver limit / rate | 25 / 850 / 6% | History / judgment / judgment |
| Annual debt repayment / buyback | 150 / 150 | Judgment |
| Floor-plan / term-debt interest | 4.67% / 5.44%, on opening balances | History |
| Cost of equity / terminal growth | 10% / 2.5% | Judgment |
| Shares | 17.951349 million; fixed valuation denominator | Fact, per supplied table |

Opening FY2025 balances: revenue 17,999.0; inventory 2,135.8; PP&E 3,070.4; other assets 6,371.6; cash 40.4; floor plan 2,027.0; term debt 3,572.0; other liabilities 2,127.5; equity 3,891.7. Opening revolver is zero: the supplied balances already balance without it.

Each year computes income first, then noncash balance-sheet accounts, then cash flows and cash. Interest uses opening debt balances, preventing a same-year revolver-interest circularity. Impairment reduces income and other assets but is added back in cash flow. PP&E increases by capex and decreases by depreciation. Equity increases by net income and decreases by buybacks.

FCFE is net income plus depreciation and impairment, less capex, inventory growth, other working-capital growth and term-debt repayment, plus the floor-plan increase. Buybacks reduce cash and equity after FCFE. The revolver fills a cash shortfall only up to its limit; subsequent surplus cash repays it before accumulating. An unmet cash minimum blocks valuation. FCFE for the required valuation is measured before revolver changes; the baseline does not draw the revolver.

The terminal formula adds back the final 150 repayment before growing FCFE at 2.5%, exactly as prescribed. This assumes the fixed annual term-debt paydown ceases in the terminal calculation. FCFE is discounted at the cost of equity; no additional cash/debt bridge is applied. Shares remain the supplied fixed denominator; no repurchase price was supplied to project a changing share count.

## Known-answer validation

All supplied checkpoints match at their displayed precision.

| Line | FY2026E | FY2030E |
|---|---:|---:|
| Revenue | 18,323.0 | 19,678.3 |
| Operating income | 844.2 | 971.4 |
| Net income | 413.6 | 527.5 |
| FCFE | 211.4 | 342.3 |
| Year-end cash | 101.8 | 719.8 |
| Assets − liabilities − equity | 0.0 | 0.0 |

Every projected year balances within $0.0000001 million floating-point tolerance and exceeds the 25 cash minimum. The baseline revolver stays zero. Additional executable checks exercise a revolver draw, opening-balance revolver interest, subsequent repayment priority, and rejection when the credit limit cannot fund minimum cash.

The deliberate break substitutes opening cash of 40.4 for FY2026E computed cash. The model refuses with:

```text
MODEL REFUSED: FY2026E: assets - liabilities - equity gap -61.4
```

`assert_balanced` recomputes totals from the actual balances, so a stored check cannot hide the altered cash. The valuation function calls this guard before calculating value.

## Explanation and reflection

**The three operating judgments:** revenue growth controls sales volume in dollars; gross margin controls the gross profit earned from those sales; SG&A as a share of gross profit controls how much remains after overhead. Holding gross margin at 17.05% and reducing the SG&A ratio to 64.5% assumes improved operating efficiency. These are supplied classroom judgments, not claims that Bernat independently researched or defended them. Discount rate and terminal growth also materially affect value, particularly because 79.76% comes after 2030.

**Why cash is last:** earnings, investment in inventory and PP&E, borrowing, debt repayment and buybacks all affect cash. Cash therefore follows the cash-flow calculation. It is not forced to make the balance sheet balance; the separate accounting check tests whether the linked statements agree.

**What −61.4 tells us:** assets are short of liabilities plus equity by 61.4 million. In this controlled test, that exactly equals the omitted positive change in cash: 101.8 minus 40.4. It points directly to cash being left at its opening balance. In an unknown model, the same gap alone would not uniquely identify the error.

**Floor-plan financing:** these are inventory loans from manufacturers' finance arms or banks. Here, their closing balance follows inventory, interest is charged on the opening balance, and the change in financing offsets part of inventory's cash use. The course places that change in operating cash flow; this simplified convention is not a claim about every issuer's reporting classification.

Removing inventory financing means cash must fund more inventory, potentially requiring another source of credit. However, simply omitting the incremental floor-plan cash-flow line is different from removing the entire opening loan and repaying it. This case's cumulative floor-plan increase is about 189.5 million, so deleting only those increases cannot by itself explain a roughly $1.1 billion cash deficit. The video's exact removal scenario was not supplied; that numerical claim has not been independently reproduced. A consistent no-floor-plan scenario must specify what happens to existing loans, interest, and replacement financing.

## Checkout and remaining student activities

Upload `proforma.py` and `Lab09_ABG.md` together to the course GitHub repository and submit their actual file links. No GitHub remote is configured in this local course folder, and no upload or submission is claimed.

The implementation and local break test are complete. Bernat confirmed that his partner already explained the exercise. The local break test does not establish that a separate partner's file was run. Thursday's task will replace the ABG assumptions with the student's company evidence.

## Disclaimer

I am a student, not a financial professional. This document was prepared for FIN 43900 (AI Finance Applications, Purdue) as a class learning exercise. It is not professional investment research or financial advice. I used OpenAI Codex to help with research, analysis, calculations, and drafting. Any remaining errors are my own.
