#!/usr/bin/env python3
"""
Nouvelles Annales question 1446 (anonymous, 1883, p. 432), unsolved in the journal as of 31 Dec 1917.

Statement (umbral notation, B^k -> B_k, eps^k -> eps_k): with the Bernoulli numbers defined by (B+1)^p - B^p = 0
and the "Euler numbers" eps by (eps+1)^p + (eps-1)^p = 0, prove
   (2B+1)^p = (2 - 2^p) B_p,
   (4B+1)^p = (2 - 2^p) B_p - p eps_{p-1},
   (4B+3)^p = (2 - 2^p) B_p + p eps_{p-1}.
The script determines the conventions from the defining relations themselves (B_0 = 1 gives B_1 = -1/2; the eps
relation with eps_0 = 1 gives eps_1 = 0, eps_2 = -1, eps_4 = 5, ... i.e. the classical Euler/secant numbers
E_{2k} with the sign convention E_2 = -1) and then checks the three identities for p = 1..40.
Run: python3 -E -P verify/nam_q1446.py
"""
from fractions import Fraction
from math import comb

P = 42
# Bernoulli numbers from (B+1)^p - B^p = 0 for p >= 2, i.e. sum_{k<p} C(p,k) B_k = 0, B_0 = 1  -> B_1 = -1/2
B = [Fraction(1)]
for p in range(2, P + 2):
    B.append(-sum(comb(p, k) * B[k] for k in range(p - 1)) / p)
# "Euler numbers" from (e+1)^p + (e-1)^p = 0 for p >= 1 with e_0 = 1: 2 sum_{k = p, p-2, ...} C(p,k) e_k = 0 fixes e_p
E = [Fraction(1)]
for p in range(1, P + 2):
    s = sum(comb(p, k) * E[k] for k in range(p - 2, -1, -2))
    E.append(-s)
assert E[1] == 0 and E[2] == -1 and E[4] == 5 and E[6] == -61, E[:8]
print("conventions: B_1 =", B[1], "; eps_0..eps_8 =", [str(x) for x in E[:9]])


def umbral(c, d, p):
    """(c B + d)^p with B^k -> B_k"""
    return sum(comb(p, k) * c ** k * d ** (p - k) * B[k] for k in range(p + 1))


for p in range(1, P):
    r = (2 - 2 ** p) * B[p]
    assert umbral(2, 1, p) == r, ("(2B+1)^p", p)
    assert umbral(4, 1, p) == r - p * E[p - 1], ("(4B+1)^p", p)
    assert umbral(4, 3, p) == r + p * E[p - 1], ("(4B+3)^p", p)
print(f"PASS: the three symbolic relations of question 1446 hold for p = 1..{P - 1} (B_1 = -1/2 convention)")
