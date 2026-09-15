"""Lab 07: frozen Asbury P/E comparison. Run with python3 comps.py."""

# Editable inputs: USD per share; FY2024 total GAAP diluted EPS.
# Prices: December 31, 2024 close. Source: supplied Lab 07 case screenshots.
TARGET = {"ticker": "ABG", "name": "Asbury Automotive", "price": 243.03, "eps": 21.50}
PEERS = [
    {"ticker": "AN", "name": "AutoNation", "price": 169.84, "eps": 16.92, "policy": "use"},
    {"ticker": "GPI", "name": "Group 1 Automotive", "price": 421.48, "eps": 36.81, "policy": "qualify"},
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


def main():
    result = analyze(TARGET, PEERS)
    print("Lab 07 — Asbury comparable-company P/E")
    print("Frozen 2024 year-end prices / subsequently reported FY2024 total GAAP diluted EPS")
    print("Retrospective training comparison; not information available at year-end.")
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
