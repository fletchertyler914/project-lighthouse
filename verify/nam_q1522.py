#!/usr/bin/env python3
"""
Nouvelles Annales question 1522 (anonymous, 1885, p. 240), unsolved in the journal as of 31 Dec 1917.

Statement: the determinant of order n-1 whose (i,j) entry is the number of common divisors of i+1 and j+1
(i, j = 1..n-1) equals the number of squarefree integers <= n.

Check: exact computation for n <= 60.  Proof sketch: with C the (n x n) 0/1 matrix c_{ik} = [k | i] (i, k = 1..n),
(C C^T)_{ij} = #common divisors of i and j; C is unitriangular so det(C C^T) = 1 for indices 1..n (H. J. S. Smith,
Proc. LMS 7, 1875-76).  Deleting row/column 1 (the index 1) gives the (n-1)-minor asked for; by the Cauchy-Binet
expansion of det(C' C'^T) over (n-1)-subsets of columns, the surviving terms are the subsets of {1..n} whose
omitted column k gives a nonsingular C with column k removed, and exactly the squarefree k contribute 1 each.
(The script checks the determinant claim exactly; the proof sketch is not re-derived in code.)
Run: python3 -E -P verify/nam_q1522.py
"""
from math import gcd
import sympy as sp


def tau(n):
    return sum(1 for d in range(1, n + 1) if n % d == 0)


def squarefree(n):
    return all(n % (p * p) for p in range(2, int(n ** 0.5) + 1))


for n in range(2, 61):
    M = sp.Matrix(n - 1, n - 1, lambda i, j: tau(gcd(i + 2, j + 2)))
    det = M.det(method="bareiss")
    Q = sum(1 for k in range(1, n + 1) if squarefree(k))
    assert det == Q, (n, det, Q)
print("PASS: det[ tau(gcd(i,j)) ]_{i,j=2..n} = #squarefree integers <= n, for 2 <= n <= 60")
