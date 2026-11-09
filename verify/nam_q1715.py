#!/usr/bin/env python3
"""
Nouvelles Annales question 1715 (J. Franel, 1896, p. 48), unsolved in the journal as of 31 Dec 1917.

Statement: Q(n) = mu(1)^2 + ... + mu(n)^2 (the number of squarefree integers <= n) equals (6/pi^2) n + delta with
|delta| < 3 sqrt(n).

Proof (standard, Gegenbauer 1885 gives the O(sqrt n) error term):
  Q(n) = sum_{d <= sqrt n} mu(d) floor(n/d^2)
       = n sum_{d <= sqrt n} mu(d)/d^2 - sum_{d <= sqrt n} mu(d) {n/d^2}
       = (6/pi^2) n - n sum_{d > sqrt n} mu(d)/d^2 - sum_{d <= sqrt n} mu(d) {n/d^2}.
  |second term| <= n sum_{d > sqrt n} 1/d^2 < n / (sqrt n - 1) ... <= n * (1/(floor(sqrt n))) <= n/(sqrt n - 1),
  |third term| <= sqrt n.   For n >= 9: n/(sqrt n - 1) <= 1.5 sqrt n, so |delta| <= 2.5 sqrt n < 3 sqrt n;
  n < 9 is checked directly.  (Sharper: n sum_{d>x} 1/d^2 < n/(x) with x = floor(sqrt n) >= sqrt n - 1.)
This script checks the inequality exactly for all n <= 2*10^6 and reports the worst ratio |delta|/sqrt(n).
Run: python3 -E -P verify/nam_q1715.py
"""
import math

N = 2_000_000
sf = bytearray([1]) * (N + 1)
for p in range(2, int(N ** 0.5) + 1):
    for k in range(p * p, N + 1, p * p):
        sf[k] = 0
c = 6 / math.pi ** 2
Q = 0
worst = 0.0
worst_n = 0
for n in range(1, N + 1):
    Q += sf[n]
    delta = Q - c * n
    r = abs(delta) / math.sqrt(n)
    if r > worst:
        worst, worst_n = r, n
    assert abs(delta) < 3 * math.sqrt(n), (n, delta)
print(f"PASS: |Q(n) - 6n/pi^2| < 3 sqrt(n) for all n <= {N}; worst ratio {worst:.4f} at n = {worst_n}")
