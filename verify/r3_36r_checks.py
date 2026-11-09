# Riemann, Cod. Ms. B. Riemann 3 (Primzahlen) fol. 36r: numerical checks of the written values.
import mpmath as mp
mp.mp.dps = 30
C = mp.euler
S = 1 - (mp.log(4*mp.pi) - C)/2            # sum over zeros 1/(alpha^2+1/4) (Hadamard / xi'/xi(0) identity)
print("sum 1/(a^2+1/4) exact  =", mp.nstr(S, 22), " Riemann: 0.02309 57089 66121 03381")
# direct partial sum over first zeros as a sanity check (converges slowly; tail ~ log T / T)
part = mp.fsum(1/(mp.im(mp.zetazero(k))**2 + mp.mpf(1)/4) for k in range(1, 201))
print("partial sum, 200 zeros  =", mp.nstr(part, 12), "(should approach the above from below)")
print("log pi =", mp.nstr(mp.log(mp.pi), 22), " Riemann: 1.14472 98858 49400 17415")
print("log 4  =", mp.nstr(mp.log(4), 22), " Riemann: 1.38629 43611 19890 61883")
print("(log 4pi - C)/2 =", mp.nstr((mp.log(4*mp.pi)-C)/2, 22), " Riemann: 0.97690 42910 33878 96618")
# von Mangoldt explicit formula psi(x) = x - sum_rho x^rho/rho - 1/2 log(1-x^-2) - log 2pi : test at x = 100.5
x = mp.mpf('100.5')
psi = mp.fsum(mp.log(p) for n in range(2, 101) for p in [n] if all(n % d for d in range(2, int(n**0.5)+1)) for _ in [0])
# psi(x) = sum over prime powers p^k <= x of log p
def psi_exact(x):
    tot = mp.mpf(0)
    for p in range(2, int(x)+1):
        if all(p % d for d in range(2, int(p**0.5)+1)):
            pk = p
            while pk <= x:
                tot += mp.log(p); pk *= p
    return tot
zs = [mp.zetazero(k) for k in range(1, 801)]
rhs = x - mp.fsum(2*mp.re(x**r/r) for r in zs) - mp.log(1-x**-2)/2 - mp.log(2*mp.pi)
print("psi(100.5) exact =", mp.nstr(psi_exact(x), 10), " explicit formula with 800 zero pairs =", mp.nstr(rhs, 10))
# Gauss sums: |tau|^2 = q and tau(chi)tau(chibar) = chi(-1) q, for q=7, cubic character
q, g = 7, 3
ind = {pow(g, k, q): k for k in range(q-1)}
for al in [mp.exp(2j*mp.pi/3), mp.exp(2j*mp.pi/6)]:
    t1 = mp.fsum(mp.exp(2j*mp.pi*n/q)*al**ind[n] for n in range(1, q))
    t2 = mp.fsum(mp.exp(2j*mp.pi*n/q)*al**(-ind[n]) for n in range(1, q))
    print("q=7 char: |tau|^2 =", mp.nstr(abs(t1)**2, 12), " tau*tau' vs q*alpha^((q-1)/2):", mp.nstr(abs(t1*t2 - q*al**((q-1)//2)), 5))
