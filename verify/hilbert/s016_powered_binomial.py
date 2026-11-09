"""Check Hilbert's diary claim (600/2 p.48): P_{n,a}(x) = sum_k C(n,k)^a x^k has
(a) only real roots for a > 1, (b) only non-real roots for a < 1 (except x=-1, n odd)."""
import mpmath as mp
from math import comb
mp.mp.dps = 60

def n_real(n, a):
    coeffs = [mp.mpf(comb(n, k)) ** a for k in range(n, -1, -1)]      # highest degree first
    roots = mp.polyroots(coeffs, maxsteps=400, extraprec=400)
    return sum(1 for r in roots if abs(mp.im(r)) < mp.mpf(10) ** -25 * (1 + abs(r)))

print("(a) real-root counts for a slightly above 1 (real-rooted means count == n):")
for a in (1.01, 1.05, 1.1, 1.2, 1.3, 1.5):
    row = [f"{n}:{n_real(n, a)}" for n in range(2, 17)]
    print(f"  a={a:<5}", " ".join(row))

print("\nthreshold a*(n) = smallest a>1 with all roots real (bisection, assumes monotone):")
ths = {}
for n in range(2, 27):
    lo, hi = mp.mpf(1), mp.mpf(3)
    if n_real(n, hi) != n:
        print(f"  n={n}: not real-rooted even at a=3"); continue
    for _ in range(22):
        mid = (lo + hi) / 2
        if n_real(n, mid) == n: hi = mid
        else: lo = mid
    ths[n] = float(hi)
print("  " + "  ".join(f"n={n}:{v:.4f}" for n, v in ths.items()))

print("\n(b) a < 1: expected real-root count 0 (n even) / 1 (n odd); violations listed:")
bad = []
for a in (-3, -1, -0.5, 0, 0.25, 0.5, 0.75, 0.9, 0.99):
    for n in range(2, 21):
        c = n_real(n, a)
        if c != (n % 2):
            bad.append((a, n, c))
print("  violations:", bad if bad else "none (n=2..20, 9 values of a)")
