# Lab19 — explain the code

This AI-assisted walkthrough supports the no-AI explanation and partner swap that Bernat confirms completing; it is not a verbatim transcript.

Open `.agents/skills/cathie-wood-edgar/scripts/cathie_checks.py`, function `cathie_checks`.

1. Load the skill configuration unless an explicit configuration was supplied. The configuration reader rejects invalid, negative or non-finite thresholds.
2. Read first and last revenue only when there are exactly five fiscal observations. Otherwise both endpoint variables become `None`.
3. Initialize growth as unknown. A missing or nonpositive first revenue cannot be a valid denominator; a negative last revenue cannot support this growth calculation.
4. With valid endpoints, divide last revenue by first, take the fourth root, subtract one and multiply by one hundred. Five observations contain four annual intervals.
5. Read the latest row; if there are no rows, use an empty mapping. Extract its R&D and revenue with missing defaults.
6. Compute R&D/revenue only when R&D and revenue exist and revenue is positive. Missing R&D does not become zero.
7. For each metric, return `not known` if the metric is `None`. Otherwise compare the unrounded value to its configured inclusive threshold and return `pass` or `fail`.
8. Return the metrics, labeled check results and the configuration. The same result feeds the printed output, table and memo audit.

**Partner's missing-input question — prepared answer:** If R&D is absent, the code leaves the input as `None`, the ratio as `None`, and its check as `not known`. Lowering the growth threshold cannot repair that unrelated gap.

`panel.py` reuses the unchanged Lab18 extractor for the original facts and years. It selects total liabilities as an instant and R&D as an annual flow, from their prescribed tags only. Each selected value retains its tag, accession, filing date, fiscal end and raw amount. Burry compares annual OCF with net income and latest total liabilities with positive equity.

The app calls each check function on the same rows. It displays saved AI-authored memos, so it requires neither a hidden API key nor fresh runtime agent calls. A fingerprint associates each memo with its exact rows and relevant screen configuration. A changed fact or applicable threshold makes that memo stale. The number audit separately scans every displayed memo against the printed numeric tokens. It cannot detect every incorrect attribution of an otherwise printed number.

I am a student, not a financial professional. This document was prepared for FIN 43900 (AI Finance Applications, Purdue) as a class learning exercise. It is not professional investment research or financial advice. I used OpenAI Codex to help with research, analysis, calculations, and drafting. Any remaining errors are my own.
