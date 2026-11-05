# Lab19 — Legend Panel

Bernat Pascuet Cuesta · November 5, 2026

**Question:** When three investors’ skills read the same annual filing facts, where do they agree, where do they split, and would I trust the panel?

## COST known answer

The archived direct SEC download reproduces the classroom answers; no answer-table values enter the extractor. Amounts use USD and original fiscal ends.

| Investor | Check | Result |
|---|---|---|
| Buffett | ROE at least 15% every year | pass |
| Buffett | Owner earnings positive every year | pass |
| Buffett | Owner earnings grew first to last | pass |
| Cathie Wood | Revenue grew at least 15% a year first to last | fail |
| Cathie Wood | Latest R&D at least 5% of revenue | not known |
| Burry | Operating cash flow at least net income every year | pass |
| Burry | Latest liabilities no more than twice equity | pass |

Annual revenue growth is **7.51%**. R&D is not found in every displayed year. Liabilities/equity is **2.11, 1.75, 1.96, 1.64, 1.49**, in fiscal-year order. Buffett’s positive-earnings/cash record and Burry’s cash/leverage checks agree favorably; Cathie Wood’s growth hurdle fails and innovation spending remains unknown.

## Threshold probe

The growth threshold was changed within Cathie Wood’s skill configuration from **15% to 5%**, and the code was executed. Growth switches from fail to pass; R&D remains not known. The original facts are identical. The retained threshold is **15%**, preserving the assigned demanding growth screen; Bernat approved this AI-enhanced choice. The same facts receiving a new label illustrates the dependence of a screen on its design.

## Memos and numerical evidence

The three saved model memos are in `memos/`, with one additional Cathie Wood memo for the probe. Each draws only from the shared printed script output. The app displays all three verdicts and memos side by side and checks every displayed memo for unprinted numeric tokens. Automated UI tests inject an unsupported value separately into each investor’s memo and observe the flag. A fingerprint also warns if a saved memo no longer matches the active evidence or thresholds.

Buffett: provisionally own the business on financial quality. Cathie Wood: watch it because growth fails and innovation evidence is incomplete. Burry: favorable cash-quality screen, investigate further. These are classroom judgments inspired by each investor’s lens, not their actual opinions.

## Project2 company

VTI is selected from the confirmed VTI/BND/SGOV universe. Its dated official holdings evidence identifies NVIDIA. See `COMPANY_SELECTION.md` for the holdings date and extraction limitation. NVIDIA companyfacts were downloaded directly from SEC with Bernat's supplied name/email. The last five qualifying annual fiscal ends span 2022-01-30 through 2026-01-25. Raw downloads, selected filing/tag evidence and source hashes are preserved.

| Investor | Check | NVDA |
|---|---|---|
| Buffett | ROE at least 15% every year | pass |
| Buffett | Owner earnings positive every year | pass |
| Buffett | Owner earnings grew first to last | pass |
| Cathie Wood | Revenue grew at least 15% a year first to last | pass — 68.30% |
| Cathie Wood | Latest R&D at least 5% of revenue | pass — 8.57% |
| Burry | OCF at least net income every year | fail |
| Burry | Latest liabilities no more than twice equity | pass — 0.31 |

Buffett's model memo provisionally favors the business on financial quality, Cathie Wood's favors the growth/reinvestment screen, and Burry's says watch it and investigate earnings-to-cash divergence. All three model memos use printed numbers only and match the analyzed evidence.

The split is coherent: positive OCF minus capex does not imply OCF is at least net income. Latest OCF of 102,718 is below net income of 120,067 (USD millions), even though owner earnings remain positive at 96,676. The limited screen cannot explain that divergence or judge a purchase price.

## NVIDIA bull and bear — AI-assisted preparation

**Bull:** NVIDIA passes every Buffett and Cathie Wood check, combining positive owner earnings with annual revenue growth of 68.30% and latest R&D/revenue of 8.57%. Latest liabilities/equity of 0.31 also passes Burry's balance-sheet check, supporting further investigation of business quality.

**Bear:** Operating cash flow is below net income in several displayed years, so Burry's every-year cash-backing check fails despite the favorable growth and leverage readings. The panel cannot explain that divergence or establish a sensible purchase price, so favorable checks alone are insufficient to act.

Bernat confirms completing the partner bull/bear exchange. The written arguments are AI-assisted summaries, not verbatim partner quotations.

## Decision — AI-enhanced and approved by Bernat

Only with a condition: I would let the panel shortlist Project2 companies after verifying its SEC inputs and retaining unknowns, but I would require a human review of NVIDIA’s earnings-to-cash divergence, business risks and valuation before acting.

## Participation and validation

Twelve tests and the two new skill validators pass. `evidence/LAB19_VERIFICATION.json` records the independent known-answer comparisons and memo audits. Browser discovery returned no connected browsers, so no visual browser review is claimed. Bernat confirms the Lab19 opener, no-AI explanation/swap, partner bull/bear discussion, learning discussion and reflection are complete, and approves the threshold and conditional decision. No exact oral transcript is invented. Quiz attempt and external submission remain unverified; see `CHECKOUT.md`.

I am a student, not a financial professional. This document was prepared for FIN 43900 (AI Finance Applications, Purdue) as a class learning exercise. It is not professional investment research or financial advice. I used OpenAI Codex to help with research, analysis, calculations, and drafting. Any remaining errors are my own.
