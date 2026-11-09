#!/usr/bin/env python3
"""
Nouvelles Annales question 880 (Lionnet, 1868, p. 190), unsolved in the journal as of 31 Dec 1917.

Statement: if P is the product of the integers less than N and prime to N, then P - 1 is divisible by N whenever
N is neither a prime, nor twice a prime, nor a power of an odd prime, nor twice such a power.

This is Gauss's generalisation of Wilson's theorem (Disquisitiones Arithmeticae, 1801, art. 78): P = -1 (mod N) for
N = 4, p^k, 2p^k (p odd prime) and P = +1 (mod N) otherwise.  Lionnet's exception list ("twice a prime") covers
N = 4 = 2*2, so his statement is exactly Gauss's theorem (1801), 67 years before the question was posed.
Run: python3 -E -P verify/nam_q0880.py
"""
from math import gcd


def is_prime(n):
    return n > 1 and all(n % p for p in range(2, int(n ** 0.5) + 1))


def prime_power(n):
    for p in range(2, n + 1):
        if n % p == 0:
            while n % p == 0:
                n //= p
            return p if n == 1 else None
    return None


def exception_lionnet(N):
    """N is a prime, twice a prime, a power of an odd prime, or twice such a power."""
    if is_prime(N):
        return True
    if N % 2 == 0 and is_prime(N // 2):
        return True
    p = prime_power(N)
    if p and p % 2 == 1:
        return True
    if N % 2 == 0:
        p = prime_power(N // 2)
        if p and p % 2 == 1:
            return True
    return False


bad = []
for N in range(2, 3001):
    P = 1
    for a in range(1, N):
        if gcd(a, N) == 1:
            P = P * a % N
    if not exception_lionnet(N) and (P - 1) % N != 0:
        bad.append((N, P))
print("counterexamples to the statement as printed, N <= 3000:", bad)
assert bad == []
print("PASS: no counterexample for N <= 3000; the statement is Gauss's generalised Wilson theorem (D.A. art. 78, 1801)")
