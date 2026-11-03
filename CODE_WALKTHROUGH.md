# Lab18 — understand and explain the code

This is AI-enhanced preparation for Bernat's explanation, not evidence that the no-AI activity happened.

Open `.agents/skills/buffett-edgar/scripts/edgar.py` at `year_row`.

1. `selected` calls `select_fact` for each required metric and this fiscal-year-end date. It retains the XBRL tag and original filing information, not just a number.
2. `values` extracts the raw USD amounts; missing amounts remain Python `None`.
3. `ni, equity` and `ocf, capex` give names to the inputs to the formulas.
4. `roe` is unknown when net income or equity is missing, or equity is zero or negative. Otherwise, divide net income by year-end equity and convert to percent.
5. `owner` is missing if either operating cash flow or capex is missing. Otherwise subtract capex from operating cash flow. A negative result is retained.
6. The returned row keeps the date, values, derived metrics, source facts and formulas together.

Where does “not found” come from? `select_fact` exhausts the prescribed tags without a qualifying USD fact and returns `val: None`. `money` renders that as “not found”; it never replaces it with zero. `checks` returns “not known” when a required input is missing. Unknown ROE is also rendered “not known”.

`annual` filters 10-K duration facts to a year-length interval, allowing ordinary calendar and retail reporting years. `analyze` selects the latest annual ends rather than using `fy`, which can describe the filing year of an older comparative number. `select_fact` applies tag preference per year, then chooses the latest filing date and accession within that tag. Instant equity must have no duration start date. Amounts remain in USD for arithmetic and become USD millions only when displayed.

The number audit extracts numeric tokens from the entire memo and compares them to printed script tokens. Commas and trailing decimal zeros normalize; a percent remains distinct from an ordinary amount. An injected unprinted percentage is flagged. This catches unsupported numbers but cannot detect a printed amount copied into the wrong year or an unsupported qualitative assertion.

A skill is a folder containing a manifest and optional scripts. Codex first sees a small name/description to decide relevance, loads the instructions when needed, and executes or reads supporting files as appropriate. This saves context and reduces interference from unrelated skills. The script fixes extraction, formulas and checks for a given input snapshot; the AI still chooses and explains the business judgment. Future SEC data revisions can legitimately change later runs, which is why saved raw files and hashes matter.

Numbers belong in code because selection and arithmetic need traceable, repeatable rules. The model interprets limited evidence; it must not manufacture missing financial inputs. “Not found” states the actual evidence boundary. An estimate would pretend the prescribed tag exists and make the check look more complete than it is.

Before class checkout, explain this without AI to your partner, answer where missing values originate, and swap roles. Bernat subsequently confirmed all Lab18 partner activities were completed; this walkthrough remains preparation rather than a transcript.

I am a student, not a financial professional. This document was prepared for FIN 43900 (AI Finance Applications, Purdue) as a class learning exercise. It is not professional investment research or financial advice. I used OpenAI Codex to help with research, analysis, calculations, and drafting. Any remaining errors are my own.
