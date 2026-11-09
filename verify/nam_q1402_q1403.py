#!/usr/bin/env python3
"""
Nouvelles Annales questions 1402 and 1403 (E. Cesàro, 1882, p. 240), listed unsolved in 1915.

1402: "La somme des p-ièmes puissances des diviseurs de n est égale, en moyenne, à n^p (1 + 1/2^{p+1} + 1/3^{p+1} + ...)".
1403: "a, b, c, ... étant les diviseurs de n, on a, en moyenne,  p/(a+p) + p/(b+p) + ... = 1 + 1/2 + ... + 1/p".

Reading "en moyenne" in Cesàro's usual sense (arithmetic mean over n = 1..N, N -> infinity), both are two-line
Dirichlet-average identities:

  1403:  (1/N) sum_{n<=N} sum_{d|n} p/(d+p) = (1/N) sum_{d<=N} floor(N/d) p/(d+p)  ->  sum_{d>=1} p/(d(d+p))
         and p/(d(d+p)) = 1/d - 1/(d+p), which telescopes to H_p = 1 + 1/2 + ... + 1/p.   (exact limit)

  1402:  (1/N) sum_{n<=N} sigma_p(n)/n^p = (1/N) sum_{n<=N} sum_{dk=n} 1/k^p = (1/N) sum_{k<=N} floor(N/k)/k^p
         -> sum_{k>=1} 1/k^{p+1} = zeta(p+1);  i.e. sigma_p(n) is "on average" n^p zeta(p+1)
         (this is the standard average order of sigma_p, e.g. Hardy & Wright, Theorem 324, for p >= 1).

This script checks the telescoping identity symbolically and both means numerically.
Run:  python3 -I verify/nam_q1402_q1403.py
"""
import math
import sympy as sp

d, p = sp.symbols("d p", positive=True)
# telescoping identity behind 1403
assert sp.simplify(p / (d * (d + p)) - (1 / d - 1 / (d + p))) == 0
for pp in range(1, 7):
    s = sp.summation(1 / d - 1 / (d + pp), (d, 1, sp.oo))
    assert sp.simplify(s - sp.harmonic(pp)) == 0, (pp, s)
print("PASS 1403: sum_{d>=1} p/(d(d+p)) = H_p symbolically for p = 1..6")

N = 200000
for pp in (1, 2, 3, 5):
    tot = 0.0
    for dd in range(1, N + 1):
        tot += (N // dd) * pp / (dd + pp)
    mean = tot / N
    H = sum(1 / k for k in range(1, pp + 1))
    err = abs(mean - H)
    print(f"1403 p={pp}: mean over n<=N of sum_(d|n) p/(d+p) = {mean:.6f}, H_p = {H:.6f}, |diff| = {err:.2e} (bound 5 p ln N / N)")
    assert err < 5 * pp * math.log(N) / N   # tail of the series plus the floor(N/d) rounding, both O(p log N / N)
print("PASS 1403 numerically (error is the O(p/N) tail of the series)")

for pp in (1, 2, 3):
    tot = 0.0
    for k in range(1, N + 1):
        tot += (N // k) / k ** pp
    mean = tot / N
    z = float(sp.zeta(pp + 1))
    err = abs(mean - z)
    print(f"1402 p={pp}: mean over n<=N of sigma_p(n)/n^p = {mean:.6f}, zeta(p+1) = {z:.6f}, |diff| = {err:.2e}")
    assert err < 1e-3
print("PASS 1402 numerically: mean of sigma_p(n)/n^p -> zeta(p+1)")
