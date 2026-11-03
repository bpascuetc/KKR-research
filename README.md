# Lab18 — Buffett as a repeatable skill

Bernat Pascuet Cuesta · FIN 43900 · November 3, 2026

The app separates reproducible SEC calculations from a saved, explicitly Buffett-inspired AI judgment. No stock prices, paid data services or FAskills installation are used.

## Verified handoff

Direct SEC downloads reproduce every supplied COST cell and all three passing checks. JPM's prescribed capex/owner-earnings gaps and unknown checks are preserved. Both model memos contain only printed numbers; a hand-typed unprinted ROE is flagged. Six automated tests and an additional app check on the actual downloaded data pass. See `evidence/verification.json` and `evidence/UI_VERIFICATION.json`.

Bernat confirms partner activities are complete and handles submission. Bernat approved the AI-enhanced COST trust line and supplied the separate browser-AI response. All its displayed financial inputs, fiscal dates and ROEs match our SEC output; its broader source choices and unverified narrative claims are distinguished in BROWSER_COMPARISON.md.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export SEC_USER_AGENT='Your full name your.real@email.edu'
python .agents/skills/buffett-edgar/scripts/edgar.py COST
python .agents/skills/buffett-edgar/scripts/edgar.py JPM
python -m streamlit run app.py --server.port 8502
```

Replace the example contact with your own. The script rejects a missing contact. A refresh needs network access; saved SEC files can be replayed without a connection:

```bash
python .agents/skills/buffett-edgar/scripts/edgar.py COST --offline
python -m unittest test_lab18.py -v
python verify_live.py
```

On Bernat's machine, the existing Python environment at `../../Lab15/2026-10-22/.venv/bin/python` from this directory already contains Streamlit, pandas and certifi; no second environment is necessary.

## Use the skill

The complete skill is committed at `.agents/skills/buffett-edgar/`. On Bernat's machine it is also linked into `~/.agents/skills/buffett-edgar`, a user skill discovery location. Open this lab folder in Codex and request:

> Use $buffett-edgar on COST. Use my SEC contact, save evidence here, read the script output, write memos/COST_memo.md, then validate its numbers. Repeat for JPM and explain its unavailable owner earnings.

If the skill does not appear, restart Codex. Its instructions and script travel together in the repository. The app reads the saved memo; it does not use a hidden API key or pretend a Python template is a new AI judgment. For a new ticker, run the skill to create that ticker's memo.

## Inspect

- `evidence/*_companyfacts.json`: raw SEC response; matching `.source.json` files give source URL, retrieval time and SHA-256.
- `evidence/*_results.json`: selected USD facts and computed ratios/checks, including tag/period/filing/accession provenance.
- `evidence/*_printed.md`: the exact numeric evidence allowed in the memo, with display values in USD millions.
- `memos/*_memo.md`: model judgments, with the approved COST student trust decision labeled separately.
- `verify_live.py`: the instructor's COST table as a comparison oracle only. The downloader and extractor never read these anchors.
- `test_lab18.py`: synthetic annual-period, revision, tag, missing-data and number-audit edge cases plus Streamlit interaction tests. Synthetic data is temporary and never enters submitted SEC evidence.
- `CHECKOUT.md`: technical evidence, student confirmations and submission status.

## Rules and limits

Only USD facts filed on form 10-K qualify. Annual flows use a duration near a year, including retail reporting years. Fiscal periods are labeled by their actual end dates, not the year of the filing containing a comparative amount. The required tag takes precedence over its fallback for each period; the latest filing within that tag/period wins. The last annual flow ends identify the five displayed years; instant year-end equity is matched to those dates. No value is estimated or substituted from an unapproved tag.

ROE uses year-end equity; nonpositive/missing equity makes it unknown. Owner earnings are the lab's OCF-minus-capex proxy, not a maintenance-capex reconstruction. An unavailable required input makes the corresponding check unknown. Endpoint growth needs both endpoints, while the positive-every-year check needs every annual amount.

The memo audit compares normalized printed numeric tokens, preserving percentages as a distinct type. It catches an injected unprinted value but cannot prove metric/year attribution or establish moat, management quality or a purchase price. Review those claims separately. A later SEC revision may change a refreshed result; archived downloads preserve reproducibility. Live discrepancies from the classroom answer must be disclosed, not patched with the answer table.

The supplied fresh-browser-AI response and comparison are recorded in BROWSER_COMPARISON.md. Partner activities are student-confirmed; app tests do not serve as evidence of oral participation. GitHub upload and Brightspace checkout are Bernat's steps.

I am a student, not a financial professional. This document was prepared for FIN 43900 (AI Finance Applications, Purdue) as a class learning exercise. It is not professional investment research or financial advice. I used OpenAI Codex to help with research, analysis, calculations, and drafting. Any remaining errors are my own.
