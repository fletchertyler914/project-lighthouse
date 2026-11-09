"""L-033 checks (Euler, Opera postuma I, E806 pp. 202-203, 242, 251). Pure computation; run with python3 -I."""
from math import gcd, isqrt
import random

# (a) Ramanujan-Nagell: ((1+sqrt(-7))/2)^n = (a_n + b_n sqrt(-7))/2 ; a_{n+1} = (a_n - 7 b_n)/2, b_{n+1} = (a_n + b_n)/2
a, b = 1, 1
hits = []
for n in range(1, 20001):
    if abs(b) == 1:
        hits.append(n)
    a, b = (a - 7 * b) // 2, (a + b) // 2
print("(a) b_n = +-1 for n <= 20000:", hits)
sols = [m for m in range(3, 300) if isqrt(2 ** m - 7) ** 2 == 2 ** m - 7]
print("    2^m - 7 is a square for m < 300:", sols, "| 181^2 + 7 == 2^15:", 181 ** 2 + 7 == 2 ** 15)
a, b = 1, 1
for n in range(1, 213):
    a, b = (a - 7 * b) // 2, (a + b) // 2
print("    Euler's continued-fraction guess n = 213: b_213 =", b, "-> is 2^215 - 7 a square?", isqrt(2**215 - 7)**2 == 2**215 - 7)


# (b) Tunnell (1983). For squarefree n: if n is congruent then (unconditionally)
#     odd n : #{x^2+2y^2+8z^2=n} = 2 #{x^2+2y^2+32z^2=n}
#     even n: #{x^2+4y^2+8z^2=n/2} = 2 #{x^2+4y^2+32z^2=n/2}
#     (the converse needs BSD). So "condition fails" => certainly NOT congruent.
def cnt(n, p, q):
    c = 0
    lim = isqrt(n)
    for x in range(-lim, lim + 1):
        rx = n - x * x
        for y in range(-lim, lim + 1):
            r = rx - p * y * y
            if r < 0:
                continue
            if r % q == 0:
                z2 = r // q
                z = isqrt(z2)
                if z * z == z2:
                    c += 1 if z == 0 else 2
    return c


def tunnell_ok(n):
    """True: necessary condition holds (congruent iff, under BSD). False: definitely not congruent."""
    if n % 2:
        return cnt(n, 2, 8) == 2 * cnt(n, 2, 32)
    h = n // 2
    return cnt(h, 4, 8) == 2 * cnt(h, 4, 32)


print("(b) Tunnell necessary condition: 73 ->", tunnell_ok(73), "| 146 ->", tunnell_ok(146))
print("    sanity (known congruent 5,6,7,41,157):", [tunnell_ok(k) for k in (5, 6, 7, 41, 157)],
      "| known non-congruent 1,2,3,17,33:", [tunnell_ok(k) for k in (1, 2, 3, 17, 33)])
primes = [p for p in range(3, 400) if all(p % d for d in range(2, isqrt(p) + 1))]
fails = [p for p in primes if not tunnell_ok(p) and not tunnell_ok(2 * p)]
print("    odd primes p < 400 with neither p nor 2p congruent (unconditional):", fails)
print("    residues mod 8 of those:", sorted(set(p % 8 for p in fails)))

# (c) Barlow-Abel lemma: coprime c > b > 0, odd prime n: gcd(c-b, (c^n-b^n)/(c-b)) is 1 or n, and = n iff n | (c-b).
random.seed(1)
bad = 0
trials = 0
for _ in range(5000):
    n = random.choice([3, 5, 7, 11, 13])
    c = random.randint(2, 80)
    b = random.randint(1, c - 1)
    if gcd(b, c) != 1:
        continue
    trials += 1
    g = gcd(c - b, (c ** n - b ** n) // (c - b))
    if g not in (1, n) or (g == n) != ((c - b) % n == 0):
        bad += 1
print("(c) gcd lemma: trials", trials, "violations", bad,
      "-> if a^n + b^n = c^n with n not dividing a, then c - b and its cofactor are coprime n-th powers (c - b = r^n); same for a + b, c - a")
