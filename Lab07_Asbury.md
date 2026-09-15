# Lab 07 — Comparable-company policy and implied range

Bernat Pascuet Cuesta · FIN 43900 · September 15, 2026

## Result and scope

Using the instructor's frozen Asbury case inputs, the two-peer P/E comparison gives an implied Asbury price range of **$215.81–$246.18**, with a **$231.00 median-implied price**. Removing Group 1 reduces the estimate by **$15.18** to **$215.81** and leaves only one reference estimate, with no peer range.

The numerical exercise, validation, peer-policy explanations and interpretation are complete. The student reports completing the before-AI activities. The explanations below were independently developed with AI assistance from primary company disclosures; they are not presented as a transcript of the student's earlier discussion. The instructor's frozen calculation inputs are unchanged.

## Reopen the Week 3 DCF

The existing KKR calculation was rerun during this conversation using `python3 dcf.py --kkr` from the course root. It reproduces **$68.92/share**, a **$59.65–$84.30** sensitivity range, and **28.1892%** annual FCFF growth required to reproduce its frozen $100.87 reference quote. Starting FCFF, explicit growth, the discount rate, terminal growth, and the separate equity bridge drive that valuation. Approximately 73.4% of asset-management enterprise value comes from the discounted terminal value, explaining its sensitivity to long-run assumptions.

These KKR values provide continuity with Week 3. Today's peer exercise concerns Asbury; comparing the two companies' dollar-per-share valuation ranges would not be meaningful. Lab 08 applies the peer method to the student's own company.

## What P/E measures

Price per share is the market price of one common share. Diluted earnings per share allocates earnings attributable to common shareholders across the weighted-average diluted share count, reflecting dilutive potential shares under the applicable accounting rules.

**P/E = price per share ÷ diluted EPS.** A 10× multiple means investors pay $10 for each $1 of annual earnings represented by that EPS. It does not guarantee a ten-year payback: accounting earnings are not necessarily cash distributions and future earnings can change.

Dividing by earnings helps compare differently sized companies. Applying a comparable company's P/E to the target's EPS asks what the target's share price would be under that earnings valuation. This adds a market-based cross-check to a DCF's explicit forecasts and discounting assumptions. It does not independently prove intrinsic value; peers can all be mispriced.

Comparisons should align the price date, earnings period, accounting definition, and diluted-share basis. Growth, risk, leverage, earnings quality, geography and business mix can justify different multiples. Negative or zero EPS makes this conventional positive-earnings comparison not meaningful. Unusual profits can artificially depress P/E; temporarily depressed earnings can inflate it. A lower P/E can reflect slower growth, greater risk or unsustainable earnings rather than a bargain.

## Peer policy and business evidence

**Policy: use AutoNation; qualify and retain Group 1; exclude Asbury from its own peer set.** These judgments follow business comparability, not the preferred implied price.

Asbury sells new and used vehicles, provides repair, maintenance and parts, and offers finance and insurance products. At year-end 2024 it operated 152 new-vehicle dealerships. This provides the operating baseline for selecting peers. [Asbury FY2024 results, company disclosure filed with the SEC](https://www.sec.gov/Archives/edgar/data/1144980/000114498025000008/a2024q4ex991.htm).

Franchised retail matters because dealers sell manufacturers' vehicles rather than designing and manufacturing them. Service and parts matter because they earn revenue from the installed vehicle base after the initial sale. These activities connect customer relationships, maintenance demand and vehicle sales. **Interpretation:** businesses sharing these profit sources are more informative peers than companies sharing only the broad automotive label.

| Company | Decision | Business justification and qualification |
|---|---|---|
| Asbury (ABG) | Target; exclude from peer statistics | Including the target would let its own market price influence the supposedly external benchmark. |
| AutoNation (AN) | **Use** | Its franchised dealerships sell new and used vehicles and provide maintenance, repair, parts and finance/insurance services. This is a close operating match to Asbury. AutoNation also operates used-only stores, collision centers and an auto finance company, so identical earnings quality or business mix should not be assumed. [AutoNation FY2024 Form 10-K, Item 1](https://www.sec.gov/Archives/edgar/data/350698/000035069825000029/an-20241231.htm). |
| Group 1 (GPI) | **Qualify; retain in baseline** | Its franchised dealerships and parts/service operations match the core retail model. However, it operates in both the U.S. and U.K. and acquired 54 Inchcape U.K. dealerships in August 2024. **Interpretation:** geography, currency exposure and acquisition timing make its annual earnings less directly comparable to a U.S.-focused retailer. Retain it as a useful but imperfect peer and show the result without it. [Group 1 FY2024 Form 10-K, Item 1 and acquisition discussion](https://www.sec.gov/Archives/edgar/data/1031203/000103120325000013/gpi-20241231.htm); [company acquisition announcement, August 1, 2024](https://www.sec.gov/Archives/edgar/data/1031203/000103120324000061/exhibit991-8124.htm). |

Group 1's acquisition also creates a timing consideration: its year-end market price reflects the acquired business, while FY2024 earnings include only the post-acquisition portion of its results. This is a reason for qualification, not a reason to replace the assignment's prescribed GAAP EPS with a different measure.

The evidence supports retaining both peers. No arbitrary premium, discount or weighting adjustment is applied. The calculator's editable `policy` field accepts `use`, `qualify`, or `exclude`; qualified peers remain in the baseline. Removing Group 1 is a sensitivity check, not a change in the policy justified above.

**Reflection:** P/E measures the price paid per unit of accounting earnings. AutoNation belongs because of its similar dealership and aftersales model; Group 1 belongs with qualifications because its international footprint and acquisition timing affect comparability. Even a well-chosen peer set cannot establish fair value without considering growth, risk and earnings sustainability.

## Frozen inputs and method

Source: instructor-provided Lab 07 screenshots, “Implement — reproduce the real case” and “Validate — check before trusting.” The frozen prices and EPS are taken exactly from those screenshots. Primary company disclosures were consulted only to complete the missing business explanations; no replacement price/EPS data was fetched and no packages were installed. The linked instructor worked case was not located, so the cited disclosures provide independent support for the peer policy.

| Company | December 31, 2024 closing price | FY2024 total GAAP diluted EPS |
|---|---:|---:|
| Asbury (ABG) | $243.03 | $21.50 |
| AutoNation (AN) | $169.84 | $16.92 |
| Group 1 (GPI) | $421.48 | $36.81 |

This is a retrospective training comparison: year-end prices are paired with subsequently reported annual earnings. It is not a reconstruction of information available to investors on December 31, 2024.

The calculator computes each peer's price/EPS, then the minimum, median and maximum peer multiple. Each is multiplied by Asbury's $21.50 EPS. With two peers, the median is the arithmetic average of their two multiples. Intermediate values retain Python's full floating-point precision; only displayed multiples and prices are rounded to six decimals and cents. P/E already yields an equity price per share: there is no cash/debt bridge.

Worked arithmetic: **($169.84 ÷ $16.92) × $21.50 = $215.81**, rounded only at the end.

## Validated results

| Calculation | Reproduced result |
|---|---:|
| AutoNation P/E | 10.037825× |
| Group 1 P/E | 11.450149× |
| Peer median P/E | 10.743987× |
| Asbury P/E at its frozen price | 11.303721× |
| Minimum peer-implied Asbury price | $215.81 |
| Median-implied Asbury price | $231.00 |
| Maximum peer-implied Asbury price | $246.18 |
| Remove GPI: remaining AN reference estimate | $215.81 |
| Remove GPI: change from full-peer estimate | −$15.18 |
| Remove AN: remaining GPI reference estimate | $246.18 |
| Remove AN: change from full-peer estimate | +$15.18 |

All supplied benchmark answers match. The removal changes are calculated from unrounded estimates: subtracting the displayed $215.81 and $231.00 instead would produce a one-cent rounding discrepancy.

Additional checks passed for normalized duplicate tickers, target exclusion, policy exclusions, missing tickers, missing/nonpositive/nonfinite price or EPS, one usable peer, no usable peers, and invalid target inputs. Duplicate tickers keep their first occurrence, even if invalid, and later occurrences are disclosed as skipped. Invalid target EPS prevents implied prices; an invalid target price prevents the target's own P/E and market comparison but does not prevent peer-implied prices when target EPS is valid.

## Interpret the changed peer set

Removing the higher-multiple peer, Group 1, lowers the median multiple to AutoNation's 10.037825×. Holding Asbury EPS fixed, that lowers the implied price to $215.81. With just one peer, there is no cross-company dispersion from which to form a peer range; the result is a reference estimate, not a range with identical endpoints.

The two-peer result brackets Asbury's frozen $243.03 price, which is above the median-implied estimate. This does not establish that Asbury is fairly valued or overpriced: peer selection, growth, leverage, business mix and earnings quality can explain a premium or discount, and two companies are a small comparison set. Removing Group 1 is a sensitivity exercise, not evidence that it should be excluded.

## Run and checkout

From the course folder `Documents/Courses/AIFinance2026/BernatPascuete`:

```bash
python3 Lab07/2026-09-15/comps.py
```

From this dated folder:

```bash
python3 comps.py
```

Python 3.12.3 was used successfully. The script uses only the standard library. Upload [this write-up](Lab07_Asbury.md) and [comps.py](comps.py) together to the course GitHub repository and submit their actual GitHub file URLs. Checkout files are complete. Upload the two files together to your existing GitHub account and submit their actual file URLs. The accompanying ZIP is a convenient local package; GitHub checkout requires the individual uploaded files. Publication has not been performed from this session. Bring this calculator and the Week 3 KKR DCF to Lab 08; the linked Week 4 prework was not included in these screenshots.

## Disclaimer

I am a student, not a financial professional. This document was prepared for FIN 43900 (AI Finance Applications, Purdue) as a class learning exercise. It is not professional investment research or financial advice. I used OpenAI Codex to help with research, analysis, calculations, and drafting. Any remaining errors are my own.
