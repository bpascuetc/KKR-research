"""Lab 16: point-in-time provenance gate. Standard library only.

Run: python3 asof.py
Edit TABLE and DECISION_DATE below to explore another decision date.

I am a student, not a financial professional. This document was prepared for
FIN 43900 (AI Finance Applications, Purdue) as a class learning exercise.
It is not professional investment research or financial advice. I used OpenAI
Codex to help with research, analysis, calculations, and drafting.
Any remaining errors are my own.
"""

from datetime import date
import calendar


DECISION_DATE = "2026-03-31"
# Row number, ticker, month measured, publication date, index.
TABLE = [
    (1, "AAA", "2026-01", "2026-02-10", 101.0),
    (2, "AAA", "2026-02", "2026-03-10", 104.0),
    (3, "AAA", "2026-03", "2026-04-10", 109.0),
    (4, "AAA", "2026-02", "2026-03-25", 103.0),
    (5, "BBB", "2026-01", "2026-02-10", 98.0),
    (6, "BBB", "2026-02", "2026-03-10", 97.0),
    (7, "BBB", "2026-02", "2026-03-10", 97.0),
    (8, "BBB", "2026-03", "2026-04-10", 92.0),
    (9, "CCC", "2026-01", "2026-02-10", 110.0),
    (10, "CCC", "2026-02", "2026-04-05", 112.0),
    (11, "", "2026-02", "2026-03-10", 99.0),
    (12, "CCC", "2026-02", "2026-03-10", 111.0),
]


def latest_vintages(rows):
    """Keep the latest publication per ticker/month; reject ambiguous ties."""
    latest = {}
    for row in rows:
        key = (row[1], row[2])
        previous = latest.get(key)
        if previous is not None and row[3] == previous[3] and row[4] != previous[4]:
            raise ValueError(f"Conflicting values at the same publication: {key}")
        if previous is None or row[3] > previous[3]:
            latest[key] = row
    return sorted(latest.values(), key=lambda row: row[0])


def filter_asof(table, decision_date):
    cutoff = date.fromisoformat(decision_date)
    funnel = []
    rows = list(table)

    removed = [row for row in rows if not row[1].strip()]
    rows = [row for row in rows if row[1].strip()]
    funnel.append(("1. Quarantined: no ticker", removed))

    unique, removed, seen = [], [], set()
    for row in rows:
        # Row number identifies provenance; it is not part of the data identity.
        identity = row[1:]
        if identity in seen:
            removed.append(row)
        else:
            seen.add(identity)
            unique.append(row)
    rows = unique
    funnel.append(("2. Exact duplicate", removed))
    clean = list(rows)

    removed = [row for row in rows if date.fromisoformat(row[3]) > cutoff]
    rows = [row for row in rows if date.fromisoformat(row[3]) <= cutoff]
    funnel.append(("3. Published after decision date", removed))

    panel = latest_vintages(rows)
    retained = {row[0] for row in panel}
    removed = [row for row in rows if row[0] not in retained]
    funnel.append(("4. Older vintage replaced", removed))
    # Same clean observations, but deliberately no publication-date cutoff.
    naive_panel = latest_vintages(clean)
    return funnel, panel, naive_panel


def signals(panel):
    results = {}
    for ticker in sorted({row[1] for row in panel}):
        rows = sorted((row for row in panel if row[1] == ticker), key=lambda row: row[2])
        if len(rows) < 2:
            results[ticker] = (None, rows[-1][2])
            continue
        previous, latest = rows[-2:]
        py, pm = map(int, previous[2].split("-"))
        ly, lm = map(int, latest[2].split("-"))
        if ly * 12 + lm - (py * 12 + pm) != 1 or previous[4] == 0:
            results[ticker] = (None, latest[2])
        else:
            results[ticker] = ((latest[4] / previous[4] - 1) * 100, latest[2])
    return results


def signal_text(result):
    value, month = result
    label = f"{calendar.month_name[int(month[5:])]} {month[:4]}"
    return f"{value:+.2f}% ({label})" if value is not None else f"Unavailable ({label}; need adjacent months and nonzero base)"


def main():
    funnel, panel, naive_panel = filter_asof(TABLE, DECISION_DATE)
    print(f"Decision date: {DECISION_DATE}\nInput rows: {len(TABLE)}\n\nROW FUNNEL")
    remaining = len(TABLE)
    for label, removed in funnel:
        remaining -= len(removed)
        numbers = ", ".join(str(row[0]) for row in removed) or "none"
        print(f"{label}: removed {len(removed)}; rows {numbers}; remaining {remaining}")
    print("\nAS-OF PANEL\nRow | Ticker | Month measured | Published on | Index")
    for row in panel:
        print(f"{row[0]:>3} | {row[1]} | {row[2]} | {row[3]} | {row[4]:.1f}")
    actual, naive = signals(panel), signals(naive_panel)
    print("\nSIGNALS\nTicker | As-of | Naive (ignores publication cutoff)")
    for ticker in sorted(set(actual) | set(naive)):
        left = signal_text(actual[ticker]) if ticker in actual else "Unavailable"
        right = signal_text(naive[ticker]) if ticker in naive else "Unavailable"
        print(f"{ticker} | {left} | {right}")


if __name__ == "__main__":
    main()
