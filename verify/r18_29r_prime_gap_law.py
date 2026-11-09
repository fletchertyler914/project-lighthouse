"""Cod. Ms. B. Riemann 18 fol. 29r: a law for the gaps between consecutive primes.

Page (as read on the scan):
  phi(g, x) = number of primes below x whose next prime is larger by g
  Li(x) = phi(2,x) + phi(4,x) + phi(6,x) + ...          (every prime has one next prime)
  x     = 2 phi(2,x) + 4 phi(4,x) + 6 phi(6,x) + ...    (the gaps add up to x)
  hence, treating g as continuous with spacing 2:  Li = (1/2) Int phi dg,  x = (1/2) Int phi g dg
  ansatz  phi'/phi = -Li/x  (in g)   =>   phi(g, x) = C exp(-g Li/x),   C = 2 Li^2 / x

Checks:
  1. algebra: the constant C and the second moment (sympy);
  2. data: count the gaps between consecutive primes below x = 10^6, 10^7, 10^8 and compare with the page's law.
     The true counts carry an arithmetic factor that depends on the prime factors of g (Hardy-Littlewood 1923),
     which the page ignores, so the comparison is made per gap and in bins of width 30 (= 2*3*5), which average
     most of that factor out.
Run: python3 -E -P verify/r18_29r_prime_gap_law.py   (pure computation; about a minute)
"""
import math
import sympy as sp
from mpmath import li

# ---- 1. algebra
g, L, x, C = sp.symbols("g L x C", positive=True)
phi = C * sp.exp(-g * L / x)
Csol = sp.solve(sp.Eq(sp.Rational(1, 2) * sp.integrate(phi, (g, 0, sp.oo)), L), C)[0]
print("1. normalisation gives C =", Csol, "| page: 2 Li^2/x ->", sp.simplify(Csol - 2 * L**2 / x) == 0)
second = sp.simplify(sp.Rational(1, 2) * sp.integrate((phi * g).subs(C, Csol), (g, 0, sp.oo)))
print("   (1/2) Int g phi dg =", second, "| page: x ->", sp.simplify(second - x) == 0)
print("   phi'/phi = -Li/x:", sp.simplify(sp.diff(phi, g) / phi + L / x) == 0)


# ---- 2. data
def primes_upto(n):
    sieve = bytearray([1]) * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, int(n**0.5) + 1):
        if sieve[p]:
            sieve[p * p :: p] = bytearray(len(range(p * p, n + 1, p)))
    return sieve


def gap_counts(n):
    sieve = primes_upto(n)
    counts = {}
    prev = 3                       # start at 3 so that all gaps are even, as on the page
    i = sieve.find(1, 4)
    while i != -1:
        d = i - prev
        counts[d] = counts.get(d, 0) + 1
        prev = i
        i = sieve.find(1, i + 1)
    return counts


for X in (10**6, 10**7, 10**8):
    cnt = gap_counts(X)
    Li = float(li(X))
    lam = Li / X
    law = lambda gg: 2 * Li**2 / X * math.exp(-gg * lam)
    n_gaps = sum(cnt.values())
    print("\n2. x = %.0e: %d gaps counted; Li(x) = %.0f; mean gap %.3f; page's mean x/Li = %.3f"
          % (X, n_gaps, Li, sum(k * v for k, v in cnt.items()) / n_gaps, X / Li))
    print("   single gaps (count / page's law):  " + "  ".join(
        "g=%d: %d / %.0f" % (gg, cnt.get(gg, 0), law(gg)) for gg in (2, 4, 6, 8, 10, 12, 30)))
    print("   bins of width 30:   gaps        counted   page's law   ratio")
    for lo in range(2, 152, 30):
        c = sum(cnt.get(gg, 0) for gg in range(lo, lo + 30, 2))
        m = sum(law(gg) for gg in range(lo, lo + 30, 2))
        print("                    %4d-%-4d  %10d   %10.0f   %.3f" % (lo, lo + 28, c, m, c / m if m else float("nan")))
    # twin primes: the page's law at g = 2 against Hardy-Littlewood (1923): 2*C2*Int_2^x dt/log^2 t, C2 = 0.6601618...
    hl = 2 * 0.6601618158 * ((Li - X / math.log(X)) - (float(li(2)) - 2 / math.log(2)))
    print("   twin primes below x: counted %d | page's law at g=2: %.0f | Hardy-Littlewood 1923: %.0f"
          % (cnt.get(2, 0), law(2), hl))
    big = max(cnt)
    print("   largest gap below x: %d; the law puts %.2f gaps at or beyond it"
          % (big, sum(law(gg) for gg in range(big, big + 2000, 2))))
