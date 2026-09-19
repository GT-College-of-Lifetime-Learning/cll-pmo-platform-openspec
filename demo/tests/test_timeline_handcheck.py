from datetime import date

# Spec scenario (strategy-success-dashboard): as-of Aug 16, 2026 ->
# 6.2% elapsed, 93.8% remaining, 3,425 calendar days remaining.
START = date(2026, 1, 1)
END = date(2035, 12, 31)
total = (END - START).days + 1
assert total == 3652, total

for asof, exp_elapsed, exp_remaining_days in [
    (date(2026, 8, 16), 6.2, 3425),
    (date(2026, 9, 19), None, None),  # today's demo as-of
]:
    elapsed = (asof - START).days
    remaining = (END - asof).days + 1
    pct = round(100 * elapsed / total, 1)
    print(f"as-of {asof}: elapsed {elapsed}d = {pct}%, remaining {remaining}d = {round(100-pct,1)}%")
    if exp_elapsed is not None:
        assert pct == exp_elapsed, (pct, exp_elapsed)
        assert remaining == exp_remaining_days, (remaining, exp_remaining_days)

print("hand-check PASSED: Aug 16, 2026 -> 6.2% elapsed, 3,425 days remaining (matches spec scenario)")