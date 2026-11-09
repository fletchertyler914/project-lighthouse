#!/usr/bin/env python3
"""
Nouvelles Annales question 1490 (E. Catalan, 1884, p. 384), unsolved in the journal as of 31 Dec 1917.

Statement: verify the identity
  (2a)^{n-1} - C(n-2,1)(2a)^{n-3} + C(n-3,2)(2a)^{n-5} - ...
     = C(n,1) a^{n-1} + C(n,3) a^{n-3}(a^2-1) + C(n,5) a^{n-5}(a^2-1)^2 + ...

Both sides are the Chebyshev polynomial of the second kind U_{n-1}(a) = sin(n t)/sin t with a = cos t:
  left  = sum_k (-1)^k C(n-1-k, k) (2a)^{n-1-2k}            (standard explicit form of U_{n-1}),
  right = sum_k C(n, 2k+1) a^{n-1-2k} (a^2-1)^k = Im[(a + i sin t)^n]/sin t with sin^2 t = 1 - a^2,
        = ((a + sqrt(a^2-1))^n - (a - sqrt(a^2-1))^n) / (2 sqrt(a^2-1)) = U_{n-1}(a).
The script checks the identity as an exact polynomial identity for n = 1..40 and against sympy's chebyshevu.
Run: python3 -E -P verify/nam_q1490.py
"""
import sympy as sp

a = sp.symbols("a")
for n in range(1, 41):
    left = sum((-1) ** k * sp.binomial(n - 1 - k, k) * (2 * a) ** (n - 1 - 2 * k) for k in range(0, (n - 1) // 2 + 1))
    right = sum(sp.binomial(n, 2 * k + 1) * a ** (n - 1 - 2 * k) * (a ** 2 - 1) ** k for k in range(0, (n - 1) // 2 + 1))
    assert sp.expand(left - right) == 0, n
    assert sp.expand(left - sp.chebyshevu(n - 1, a)) == 0, n
print("PASS: Catalan's identity holds as a polynomial identity for n = 1..40; both sides are U_{n-1}(a)")
