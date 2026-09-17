"""Lab 08: KKR historical GAAP P/E comparison. Run: python3 kkr_comps.py."""

# Editable inputs: USD per NYSE common share; FY2025 total GAAP diluted EPS.
# Historical closing prices: September 10, 2026. Sources/locators in Lab08_KKR.md.
COMPARISON_DATE = "2026-09-10"
FISCAL_YEAR_END = "2025-12-31"
TARGET = {"ticker": "KKR", "name": "KKR & Co. Inc.", "price": 100.87, "eps": 2.34,
          "price_date": "2026-09-10", "eps_publication_date": "2026-02-05", "currency": "USD"}
PEERS = [
    {"ticker": "APO", "name": "Apollo Global Management, Inc.", "price": 127.91, "eps": 5.54,
     "policy": "qualify", "price_date": "2026-09-10", "eps_publication_date": "2026-02-09", "currency": "USD"},
    {"ticker": "BX", "name": "Blackstone Inc.", "price": 125.41, "eps": 3.87,
     "policy": "qualify", "price_date": "2026-09-10", "eps_publication_date": "2026-01-29", "currency": "USD"},
]

import math
from statistics import median

DISCLAIMER = (
    "I am a student, not a financial professional. This document was prepared "
    "for FIN 43900 (AI Finance Applications, Purdue) as a class learning exercise. "
    "It is not professional investment research or financial advice. I used "
    "OpenAI Codex to help with research, analysis, calculations, and drafting. "
    "Any remaining errors are my own."
)


def positive(value):
    return (isinstance(value, (int, float)) and not isinstance(value, bool)
            and math.isfinite(value) and value > 0)


def analyze(target, peers):
    """Deduplicate by normalized ticker; first occurrence wins, even if invalid."""
    seen = {str(target.get("ticker", "")).strip().upper()}
    valid, notes = [], []
    for peer in peers:
        ticker = str(peer.get("ticker") or "").strip().upper()
        if not ticker:
            notes.append("Missing ticker: excluded; cannot identify/deduplicate peer.")
            continue
        if ticker in seen:
            notes.append(f"{ticker}: target or duplicate excluded (first occurrence wins).")
            continue
        seen.add(ticker)
        policy = str(peer.get("policy", "use")).strip().lower()
        if policy not in ("use", "qualify"):
            notes.append(f"{ticker}: excluded by policy ({policy}).")
            continue
        if not positive(peer.get("price")) or not positive(peer.get("eps")):
            notes.append(f"{ticker}: P/E and implied price not meaningful; price/EPS must be finite and positive.")
            continue
        pe = peer["price"] / peer["eps"]
        valid.append({"ticker": ticker, "pe": pe, "policy": policy})
    multiples = [p["pe"] for p in valid]
    midpoint = median(multiples) if multiples else None
    eps = target.get("eps")
    estimate = midpoint * eps if midpoint is not None and positive(eps) else None
    removals = []
    for peer in valid:
        remaining = [p["pe"] for p in valid if p["ticker"] != peer["ticker"]]
        price = median(remaining) * eps if remaining and positive(eps) else None
        removals.append((peer["ticker"], len(remaining), price,
                         price - estimate if price is not None else None))
    return {"peers": valid, "notes": notes, "median": midpoint,
            "estimate": estimate, "removals": removals}


def validate_basis(target, peers):
    from datetime import date
    comparison = date.fromisoformat(COMPARISON_DATE)
    fiscal_end = date.fromisoformat(FISCAL_YEAR_END)
    for row in [target, *[p for p in peers if p.get("policy", "use") in ("use", "qualify")]]:
        if row.get("currency") != "USD" or row.get("price_date") != COMPARISON_DATE:
            raise ValueError(f"{row['ticker']}: price date/currency mismatch.")
        publication = date.fromisoformat(row["eps_publication_date"])
        if not fiscal_end < publication <= comparison:
            raise ValueError(f"{row['ticker']}: annual earnings were not public on the comparison date.")


def main():
    validate_basis(TARGET, PEERS)
    result = analyze(TARGET, PEERS)
    print("Lab 08 — KKR comparable-company P/E")
    print(f"Comparison date: {COMPARISON_DATE}; USD common-share closing prices")
    print(f"Annual total GAAP diluted EPS: fiscal year ended {FISCAL_YEAR_END}")
    print("All earnings releases predate the comparison date; no adjusted EPS substitution.")
    print(f"Target inputs: {TARGET}")
    for peer in PEERS:
        print(f"Peer inputs: {peer}")
    for note in result["notes"]:
        print(note)
    eps_ok = positive(TARGET.get("eps"))
    price_ok = positive(TARGET.get("price"))
    if eps_ok and price_ok:
        print(f"Target P/E: {TARGET['price'] / TARGET['eps']:.6f}x")
    else:
        print("Target P/E and comparison with market price: not meaningful.")
    for peer in result["peers"]:
        implied = f"${peer['pe'] * TARGET['eps']:.2f}" if eps_ok else "not meaningful"
        print(f"{peer['ticker']} ({peer['policy']}): P/E {peer['pe']:.6f}x; target implied price {implied}")
    if not result["peers"]:
        print("No usable peers; no estimate or range.")
    else:
        print(f"Peer median P/E: {result['median']:.6f}x")
        if not eps_ok:
            print("Target implied prices: not meaningful; target EPS must be finite and positive.")
        elif len(result["peers"]) == 1:
            print(f"One valid peer: reference estimate ${result['estimate']:.2f}; no range.")
        else:
            values = [p["pe"] * TARGET["eps"] for p in result["peers"]]
            print(f"Implied range: ${min(values):.2f}–${max(values):.2f}")
            print(f"Median-implied price: ${result['estimate']:.2f}")
        for ticker, count, price, change in result["removals"]:
            if not count:
                print(f"Remove {ticker}: no usable peers remain; no estimate.")
            elif price is None:
                print(f"Remove {ticker}: implied price and change not meaningful (target EPS).")
            else:
                label = "reference estimate; no range" if count == 1 else "median estimate"
                print(f"Remove {ticker}: ${price:.2f}; change {change:+.2f} USD; {label}.")
    print("P/E produces an equity price directly; no cash/debt bridge is applied.")
    print("\nDisclaimer: " + DISCLAIMER)


if __name__ == "__main__":
    main()
