# Lab19 — Legend Panel

Same SEC facts, three investor lenses, an explicit human decision.

## Start the app

From this folder on Bernat's machine:

```bash
../../Lab15/2026-10-22/.venv/bin/python -m streamlit run app.py --server.port 8503
```

Open http://127.0.0.1:8503. COST loads from the archived direct SEC download. The panel shows seven checks, three saved verdicts and side-by-side editable memos. The original annual table, owner-earnings/net-income chart, source details, download controls and missing-data behavior remain available. `lab18_app.py` is an unchanged baseline copy for regression checks; Lab18's original folder is preserved.

For another machine, create a Python environment and install `requirements.txt`, then use `python -m streamlit run app.py`. Include the hidden `.agents` folder when uploading the project; it contains required code and all three skills.

## Reproduce and verify

```bash
python panel.py COST --offline --audit
python verify_panel.py
python -m unittest test_lab18.py test_lab19.py -v
```

COST matches every supplied Lab19 anchor. The threshold probe was performed by editing Cathie Wood's skill config, running it and restoring fifteen percent; `evidence/COST_probe_5_*` preserves the probe. The sidebar also exposes the probe. For any unsupported threshold or ticker, absent model memos are shown as absent rather than invented.

NVDA is already available under Saved SEC download. To fetch another company, set `SEC_USER_AGENT` to your actual name and real email, then run `python panel.py NVDA`. No fake contact or API key is used. SEC downloads save their URL, timestamp and SHA-256; offline replay verifies the raw source hash. Existing saved files are not live market updates.

## Files

- `.agents/skills/`: Buffett, Cathie Wood and Burry instructions, with code for each screen. Workspace-root discovery links point to the two new skills. Open this lab folder in Codex to use its full local bundle.
- `panel.py`: shared facts, added tags, calculations, printing, source validation, memo association and numeric audit.
- `app.py`: panel interface, chart, annual table, memo editor/probes/downloads.
- `memos/`: saved AI classroom judgments; `.source.json` associates a memo with the data and configuration. Old `COST_memo.md` and `JPM_memo.md` are retained Lab18 artifacts, not extra Lab19 investor outputs.
- `evidence/`: original SEC downloads, computed tables, baseline/probe results and verification evidence. Inherited Lab18 evidence retains its original filenames and scope.
- `COMPANY_SELECTION.md`: VTI/NVDA choice and dated holdings-source limitation.
- `CODE_WALKTHROUGH.md` and `DISCUSSION_PREPARATION.md`: explain-back, bull/bear and reflection preparation.
- `CHECKOUT.md`: actual completion and outstanding steps; it controls readiness claims.

NVIDIA is the selected VTI holding. Its live SEC panel and all three memos are complete; twelve behavioral tests pass. `Lab19_GITHUB_READY.zip` and `Lab19/UPLOAD_THIS_FOLDER` contain the prepared upload files; `Lab19_PREPARATION.zip` is the older partial snapshot. Bernat confirms the Lab19 oral activities are complete and approves the retained growth threshold and conditional trust decision. GitHub and Brightspace remain his submission steps.

The new skills adapt FAskills' philosophy pages to the lab's exact narrow formulas. No paid feed, FAskills installation, forecast, price target or actual-investor endorsement is implied. Numeric presence is not proof of correct metric/year attribution. A panel built on one dataset and one AI is not three independent factual audits.

I am a student, not a financial professional. This document was prepared for FIN 43900 (AI Finance Applications, Purdue) as a class learning exercise. It is not professional investment research or financial advice. I used OpenAI Codex to help with research, analysis, calculations, and drafting. Any remaining errors are my own.
