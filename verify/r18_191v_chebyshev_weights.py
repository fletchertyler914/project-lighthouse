"""Cod. Ms. B. Riemann 18 fol. 191v (pencil): trial weight systems for Chebyshev's method.

Chebyshev (1852): with T(x) = log [x]! = sum_n psi(x/n), a combination sum_d a_d T(x/d) equals
sum_m c_m psi(x/m) with c_m = sum_{d | m} a_d; if sum_d a_d/d = 0 the x log x terms cancel and one gets
bounds A x < psi(x) < B x. Chebyshev used a = {1:+1, 2:-1, 3:-1, 5:-1, 30:+1} (period 30).
The page writes Chebyshev's two bounds, then tries larger systems; the bottom table is headed
  J(x) - J(x/2) - J(x/3) - J(x/5) + J(x/6) - J(x/7) + J(x/105)        "210"
followed by rows of ten coefficients (0, +-1, -2), each row ending with its row number 1..14.

Check: (1) sum a_d/d = 0 for that system; (2) recompute c_m for m = 1..140 and compare with the page's rows
(as transcribed in data/riemann/transcripts/R.Naturphil/c379.json); (3) Chebyshev's constant A.
Run: python3 -I verify/r18_191v_chebyshev_weights.py
"""
from fractions import Fraction
from math import log

a = {1: 1, 2: -1, 3: -1, 5: -1, 6: 1, 7: -1, 105: 1}
print("1. sum a_d/d =", sum(Fraction(v, d) for d, v in a.items()), "(must be 0); period = lcm = 210")
c = lambda m: sum(v for d, v in a.items() if m % d == 0)
page = """1 0 0 0 0 0 0 0 0 -1
1 0 1 -1 -1 0 1 0 1 -1
-1 0 1 0 0 0 0 -1 1 -1
1 0 0 0 -1 0 1 0 0 -1
1 -1 1 0 -1 0 1 0 0 -1
0 0 1 0 0 -1 0 0 1 -1
1 0 -1 0 0 0 1 0 0 -2
1 0 1 0 -1 0 0 0 1 -1
0 0 1 -1 0 0 0 0 1 -1
0 0 0 0 0 0 1 -1 0 -1
1 0 1 0 -1 0 1 0 1 -1
0 -1 1 0 0 0 0 0 0 -1
1 0 0 0 0 -1 1 0 0 -1
1 0 0 0 -1 0 1 0 1 -2""".splitlines()
ok_rows = 0
bad = []
for k, row in enumerate(page, 1):
    want = [c(m) for m in range(10 * k - 9, 10 * k + 1)]
    got = [int(t) for t in row.split()]
    if want == got:
        ok_rows += 1
    else:
        bad.append((k, [(10 * k - 9 + i, got[i], want[i]) for i in range(10) if got[i] != want[i]]))
print("2. rows of the page's period-210 table that agree with c_m = sum_{d|m} a_d: %d of %d" % (ok_rows, len(page)))
for k, diffs in bad:
    print("   row %d differs at (m, page, computed):" % k, diffs)
A = log(2) / 2 + log(3) / 3 + log(5) / 5 - log(30) / 30
print("3. Chebyshev's constant A = log(2^(1/2) 3^(1/3) 5^(1/5) / 30^(1/30)) = %.5f; page's bounds: psi(x) > A x - (5/2) log x - 1, "
      "psi(x) < (6/5) A x + ..." % A)
main = -sum(Fraction(v, d) * 1 for d, v in a.items())
print("   main-term constant of the 210 system: -sum a_d log(d)/d = %.5f" % (-sum(v * log(d) / d for d, v in a.items())))
