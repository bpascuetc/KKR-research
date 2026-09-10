# Editable inputs: dollar amounts in USD millions; shares in millions.
# Enter rates as decimals (0.10 means 10%).
STARTING_FCFF = 100.0
YEARLY_GROWTH_RATES = (0.08, 0.06, 0.05, 0.04, 0.03)
WACC = 0.10
TERMINAL_GROWTH = 0.03
NON_OPERATING_CASH = 50.0
DEBT = 300.0
DILUTED_SHARES = 50.0


# Training defaults above are intentionally unchanged. KKR is an explicit scenario.
WACC_VALUES = [0.09, 0.10, 0.11]
TERMINAL_GROWTH_VALUES = [0.02, 0.03, 0.04]
TARGET_PRICE = 30.00
SHIFT_LOWER = -0.05
SHIFT_UPPER = 0.10
OTHER_EQUITY_VALUE = 0.0
CASE_LABEL = "TRAINING — classroom inputs, not KKR"

# USD millions; estimates and source locators are in KKR-research/KKR_reverse_DCF.md.
# Fixed FCFF proxy: (4235.479 + 703.508 - 637.855) * .75 * .70.
KKR_INPUTS = dict(
    STARTING_FCFF=2258.0943,
    YEARLY_GROWTH_RATES=(.15, .15, .15, .15, .15),
    WACC=.11, TERMINAL_GROWTH=.03,
    NON_OPERATING_CASH=4314.264, DEBT=9298.541,
    DILUTED_SHARES=945.131511,
    OTHER_EQUITY_VALUE=22845.565810236243,
    WACC_VALUES=[.10, .11, .12],
    TERMINAL_GROWTH_VALUES=[.02, .03, .04],
    TARGET_PRICE=100.87, SHIFT_LOWER=-.05, SHIFT_UPPER=.20,
    CASE_LABEL="KKR — illustrative adjusted FCFF/SOTP; unresolved inputs remain",
)


def price_at(growth_rates, wacc, terminal_growth):
    import math
    inputs = [STARTING_FCFF, NON_OPERATING_CASH, DEBT, DILUTED_SHARES,
              OTHER_EQUITY_VALUE, wacc, terminal_growth, *growth_rates]
    if not all(math.isfinite(x) for x in inputs):
        raise ValueError("Inputs must be finite.")
    if len(growth_rates) != 5 or any(g <= -1 for g in growth_rates):
        raise ValueError("Provide five growth rates, all greater than -100%.")
    if STARTING_FCFF <= 0 or DILUTED_SHARES <= 0:
        raise ValueError("This increasing-growth solver requires positive FCFF and shares.")
    if wacc <= -1 or terminal_growth <= -1 or terminal_growth >= wacc:
        raise ValueError("Require WACC > -100% and -100% < terminal growth < WACC.")
    cash_flow = STARTING_FCFF
    present_value = 0.0
    for year, growth in enumerate(growth_rates, 1):
        cash_flow *= 1 + growth
        present_value += cash_flow / (1 + wacc) ** year
    present_value += cash_flow * (1 + terminal_growth) / (wacc-terminal_growth) / (1+wacc)**5
    return (present_value + NON_OPERATING_CASH - DEBT + OTHER_EQUITY_VALUE) / DILUTED_SHARES


def reverse_shift(target, lower, upper):
    import math
    if not all(math.isfinite(x) for x in [target, lower, upper]) or lower >= upper:
        raise ValueError("Require finite target and ordered finite bounds.")
    if any(g + lower <= -1 or g + upper <= -1 for g in YEARLY_GROWTH_RATES):
        raise ValueError("Rejected bracket: an annual growth rate reaches -100% or below.")
    def shifted_price(shift):
        return price_at([g+shift for g in YEARLY_GROWTH_RATES], WACC, TERMINAL_GROWTH)
    low_price, high_price = shifted_price(lower), shifted_price(upper)
    if not low_price <= target <= high_price:
        return None
    if target == low_price:
        return lower
    if target == high_price:
        return upper
    for _ in range(100):
        mid = (lower + upper) / 2
        if shifted_price(mid) < target:
            lower = mid
        else:
            upper = mid
    answer = (lower + upper) / 2
    if abs(shifted_price(answer)-target) > 1e-7:
        raise ValueError("Solver did not reproduce the target price.")
    return answer


def print_extensions():
    print("\n" + CASE_LABEL)
    print("Sensitivity grid: value per diluted share (USD)")
    print("WACC / terminal" + "".join(f"{g:>12.1%}" for g in TERMINAL_GROWTH_VALUES))
    for w in WACC_VALUES:
        cells = []
        for g in TERMINAL_GROWTH_VALUES:
            try:
                cells.append(f"{price_at(YEARLY_GROWTH_RATES, w, g):12.2f}")
            except ValueError:
                cells.append(f"{'INVALID':>12}")
        print(f"{w:<15.1%}" + "".join(cells))
    print("\nReverse DCF: uniform shift added to all five explicit FCFF growth rates")
    print(f"Target price: ${TARGET_PRICE:.2f}; shift bounds: {SHIFT_LOWER*100:+.2f} to {SHIFT_UPPER*100:+.2f} percentage points")
    try:
        shift = reverse_shift(TARGET_PRICE, SHIFT_LOWER, SHIFT_UPPER)
        if shift is None:
            print("No solution in that bracket.")
        else:
            print(f"Solved shift: {shift*100:+.4f} percentage points")
            print("Solved annual growth rates: " + ", ".join(f"{g+shift:.4%}" for g in YEARLY_GROWTH_RATES))
            print(f"Reproduced price: ${price_at([g+shift for g in YEARLY_GROWTH_RATES], WACC, TERMINAL_GROWTH):.6f}")
    except ValueError as exc:
        print(f"Reverse DCF rejected: {exc}")
    print(f"Held fixed: starting FCFF={STARTING_FCFF:.6f}; WACC={WACC:.2%}; terminal growth={TERMINAL_GROWTH:.2%}; cash={NON_OPERATING_CASH:.6f}; debt={DEBT:.6f}; shares={DILUTED_SHARES:.6f}; other equity value={OTHER_EQUITY_VALUE:.6f}; five-year horizon and original growth-path differences.")
    print("This is one set of assumptions consistent with the price, not proof of mispricing.")
    print("\nDisclaimer: I am a student, not a financial professional. This document was prepared for FIN 43900 (AI Finance Applications, Purdue) as a class learning exercise. It is not professional investment research or financial advice. I used OpenAI Codex to help with research, analysis, calculations, and drafting. Any remaining errors are my own.")


def main():
    if TERMINAL_GROWTH >= WACC:
        raise SystemExit("Error: terminal growth must be less than WACC.")
    if len(YEARLY_GROWTH_RATES) != 5:
        raise SystemExit("Error: provide exactly five yearly growth rates.")
    if WACC <= -1:
        raise SystemExit("Error: WACC must be greater than -1.")
    if DILUTED_SHARES <= 0:
        raise SystemExit("Error: diluted shares must be greater than zero.")

    price_at(YEARLY_GROWTH_RATES, WACC, TERMINAL_GROWTH)
    annual_fcff = []
    fcff = STARTING_FCFF
    for growth in YEARLY_GROWTH_RATES:
        fcff *= 1 + growth
        annual_fcff.append(fcff)

    explicit_pv = sum(
        cash_flow / (1 + WACC) ** year
        for year, cash_flow in enumerate(annual_fcff, start=1)
    )
    terminal_value = annual_fcff[-1] * (1 + TERMINAL_GROWTH) / (
        WACC - TERMINAL_GROWTH
    )
    terminal_pv = terminal_value / (1 + WACC) ** len(annual_fcff)
    enterprise_value = explicit_pv + terminal_pv
    equity_value = enterprise_value + NON_OPERATING_CASH - DEBT + OTHER_EQUITY_VALUE
    value_per_share = equity_value / DILUTED_SHARES
    if enterprise_value == 0:
        raise SystemExit("Error: enterprise value is zero; terminal-value share is undefined.")
    terminal_share = terminal_pv / enterprise_value

    for year, cash_flow in enumerate(annual_fcff, start=1):
        print(f"FCFF Year {year} (USD millions): {cash_flow:.4f}")
    print(f"PV of five explicit FCFF (USD millions): {explicit_pv:.4f}")
    print(f"Terminal value at Year 5 (USD millions): {terminal_value:.4f}")
    print(f"PV of terminal value (USD millions): {terminal_pv:.4f}")
    print(f"Enterprise value (USD millions): {enterprise_value:.4f}")
    print(f"Equity value (USD millions): {equity_value:.4f}")
    print(f"Value per diluted share (USD): {value_per_share:.4f}")
    print(f"PV of terminal value / enterprise value (fraction): {terminal_share:.4f}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Training DCF, sensitivity and reverse DCF; optional illustrative KKR scenario.")
    parser.add_argument('--kkr', action='store_true')
    args = parser.parse_args()
    if args.kkr:
        globals().update(KKR_INPUTS)
    try:
        main()
        print_extensions()
    except ValueError as exc:
        parser.error(str(exc))
