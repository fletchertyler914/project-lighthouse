#!/usr/bin/env python3
"""
Nouvelles Annales question 774 (Prouhet, 1866, p. 384), unsolved in the journal as of 31 Dec 1917.

Statement: the number X_n^m of ways of dividing a convex m-gon into n parts by n-1 non-crossing diagonals is
    X_n^m = (1/n) * [m(m+1)...(m+n-2)/(n-1)!] * [(m-3)(m-4)...(m-n-1)/(n-1)!]
          = (1/n) * C(m+n-2, n-1) * C(m-3, n-1).
This is the Kirkman-Cayley formula (Kirkman 1857 conjecture; proved by Cayley, "On the partitions of a polygon",
Proc. London Math. Soc. 22 (1891) 237-262).  Checked here by brute-force enumeration of non-crossing diagonal sets.
Run: python3 -E -P verify/nam_q0774.py
"""
from itertools import combinations
from math import comb


def crosses(d1, d2):
    (a, b), (c, d) = sorted(d1), sorted(d2)
    return (a < c < b < d) or (c < a < d < b)


def count(m, n):
    diags = [(i, j) for i in range(m) for j in range(i + 2, m) if not (i == 0 and j == m - 1)]
    k = n - 1
    tot = 0
    for S in combinations(diags, k):
        if all(not crosses(S[i], S[j]) for i in range(k) for j in range(i + 1, k)):
            tot += 1
    return tot


def prouhet(m, n):
    num1 = 1
    for t in range(m, m + n - 1):
        num1 *= t
    num2 = 1
    for t in range(m - 3, m - n - 2, -1):
        num2 *= t
    f = 1
    for t in range(1, n):
        f *= t
    val = num1 * num2
    assert val % (n * f * f) == 0
    return val // (n * f * f)


for m in range(4, 10):
    for n in range(1, m - 1):
        c, p = count(m, n), prouhet(m, n)
        assert p == comb(m + n - 2, n - 1) * comb(m - 3, n - 1) // n
        assert c == p, (m, n, c, p)
        print(f"m={m} n={n}: enumeration {c} = formula {p}")
print("PASS: Prouhet's formula = Kirkman-Cayley number (1/n) C(m+n-2,n-1) C(m-3,n-1) for 4 <= m <= 9")
