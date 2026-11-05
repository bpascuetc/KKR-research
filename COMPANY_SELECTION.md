# Project2 company selection

The saved `Lab15/2026-10-22/updated_app/project2_mandate.json` records Bernat's confirmed VTI/BND/SGOV fund universe. VTI is the equity fund chosen for this lab; choosing one of the funds follows the assignment and does not change the portfolio.

[Vanguard's VTI holdings page](https://advisors.vanguard.com/investments/products/vti/vanguard-total-stock-market-etf) appears in the search-index extraction with holdings dated August 31, 2026. It lists NVIDIA first at 6.87%, ahead of Apple at 6.30% and Microsoft at 5.10%. The page's direct reader returned no readable body; this evidence is the indexed official-source table, not a downloaded full holdings file or a live intraday ranking. Provider dates are retained; do not call these November holdings. Other newer holdings services also listed NVIDIA first, but their weights are not imported as financial inputs.

Selected company: **NVIDIA (NVDA)**. The fund holdings evidence establishes selection only; the financial panel will use SEC companyfacts exclusively. No next-largest-company substitution is needed if its annual USD 10-K facts are retrieved.

Bernat supplied his real SEC contact email for this run. Downloaded NVIDIA companyfacts directly from SEC on November 5, 2026; its source metadata preserves the URL, retrieval time and SHA-256. The email is used only for the request, not placed in app defaults or upload instructions. NVIDIA has qualifying annual USD 10-K facts, so no fallback company is used. The completed panel and all three memos are saved in this lab.

I am a student, not a financial professional. This document was prepared for FIN 43900 (AI Finance Applications, Purdue) as a class learning exercise. It is not professional investment research or financial advice. I used OpenAI Codex to help with research, analysis, calculations, and drafting. Any remaining errors are my own.
