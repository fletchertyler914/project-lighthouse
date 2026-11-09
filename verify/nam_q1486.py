#!/usr/bin/env python3
"""
Nouvelles Annales question 1486 (anonymous, 1884, p. 192), unsolved in the journal as of 31 Dec 1917.

Statement: "the probability that the conic determined by five points taken at random in a plane is an ellipse is
infinitely small."

As stated this is not well posed ("at random in a plane" names no distribution; there is no uniform distribution
on the plane).  For any bounded region with a density, the probability is strictly positive: five points near a
circle determine an ellipse, and the ellipse condition (B^2 - 4AC < 0) is an open condition.  Monte Carlo for five
i.i.d. uniform points in the unit square and in the unit disc gives probabilities far from zero.
Run: python3 -E -P verify/nam_q1486.py
"""
import random
import numpy as np

random.seed(1)
rng = np.random.default_rng(1)


def conic_type(pts):
    # solve A x^2 + B xy + C y^2 + D x + E y + F = 0 through five points: null vector of the 5x6 design matrix
    M = np.array([[x * x, x * y, y * y, x, y, 1.0] for x, y in pts])
    _, s, vt = np.linalg.svd(M)
    A, B, C = vt[-1][:3]
    disc = B * B - 4 * A * C
    return "ellipse" if disc < 0 else "hyperbola" if disc > 0 else "parabola"


def trial(sampler, n=200000):
    cnt = {"ellipse": 0, "hyperbola": 0, "parabola": 0}
    for _ in range(n):
        cnt[conic_type(sampler())] += 1
    return {k: v / n for k, v in cnt.items()}


def square():
    return rng.random((5, 2))


def disc():
    out = []
    while len(out) < 5:
        p = rng.random(2) * 2 - 1
        if p @ p <= 1:
            out.append(p)
    return out


for name, f in (("unit square", square), ("unit disc", disc)):
    r = trial(f, 100000)
    print(f"five i.i.d. uniform points in the {name}: P(ellipse) = {r['ellipse']:.4f}, P(hyperbola) = {r['hyperbola']:.4f}")
    assert r["ellipse"] > 0.1
print("PASS: the ellipse probability is bounded away from 0 for bounded uniform distributions; the statement is false "
      "for them and undefined without a distribution")
