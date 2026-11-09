"""Checks for Trinity Add.MS a/94/18 pages 8, 71, 72 (Ramanujan)."""
from mpmath import mp, mpf, zeta, sqrt, exp, pi, cos, nprod, nsum, inf, log
mp.dps = 25
print("== p.8 (iii) powerful numbers a^2 b^3 <= x  =  sqrt(4.723034 x) - cbrt(3.10227 x) + O(x^{1/6+e})")
c1 = (zeta(mpf(3)/2)/zeta(3))**2
c2 = (zeta(mpf(2)/3)/zeta(2))**3
print("  (zeta(3/2)/zeta(3))^2 =", c1, " Ramanujan 4.723034 ->", abs(c1-mpf('4.723034')) < 1e-6)
print("  Bateman-Grosswald second term: zeta(2/3)/zeta(2) =", zeta(mpf(2)/3)/zeta(2), " cube:", c2, " Ramanujan -cbrt(3.10227) =", -mpf('3.10227')**(mpf(1)/3))
# brute-force count of powerful numbers to compare both two-term formulas
import math
def powerful_count(X):
    s=set()
    b=1
    while b**3<=X:
        a=1
        while a*a*b**3<=X:
            s.add(a*a*b**3); a+=1
        b+=1
    return len(s)
for X in (10**6, 10**7):
    N=powerful_count(X)
    R = math.sqrt(4.723034*X) - (3.10227*X)**(1/3)
    BG = float(zeta(mpf(3)/2)/zeta(3))*math.sqrt(X) + float(zeta(mpf(2)/3)/zeta(2))*X**(1/3)
    print(f"  X={X}: count={N}  Ramanujan={R:.1f}  Bateman-Grosswald={BG:.1f}")
print("== p.8 (ii) identity sqrt(2(1-1/9)(1-1/49)(1-1/121)(1-1/361)) == (1+1/7)(1+1/11)(1+1/19)?")
lhs = sqrt(2*(1-mpf(1)/9)*(1-mpf(1)/49)*(1-mpf(1)/121)*(1-mpf(1)/361)); rhs=(1+mpf(1)/7)*(1+mpf(1)/11)*(1+mpf(1)/19)
print("  ", lhs, rhs, abs(lhs-rhs)<1e-20)

print("== p.71 Euler products: F = x^2 prod(1-x^{3k})^16, F1 = x prod(1-x^{3k})^8 * E4(x^3); check Hecke relations for f = F1 + 6 sqrt(10) F")
N=60
def series_prod_pow(power):
    c=[0]*(N+1); c[0]=1
    for k in range(1,N+1):
        if 3*k>N: break
        for _ in range(power):
            for n in range(N,3*k-1,-1): c[n]-=c[n-3*k]
    return c
e8=series_prod_pow(8); e16=series_prod_pow(16)
E4=[0]*(N+1); E4[0]=1
for m in range(1,N+1):
    for j in range(1,N+1):
        if 3*m*j>N: break
        E4[3*m*j]+=240*m**3
F=[0]*(N+1); F1=[0]*(N+1)
for n in range(N+1):
    if n+2<=N: F[n+2]+=e16[n]
    s=sum(e8[i]*E4[n-i] for i in range(n+1))
    if n+1<=N: F1[n+1]+=s
import sympy as sp
r10=sp.sqrt(10)
f=[sp.nsimplify(F1[n])+6*r10*F[n] for n in range(N+1)]
print("  f_1..f_12:", [sp.simplify(v) for v in f[1:13]])
# Hecke: f_p given, f_{p^2} = f_p^2 - p^7, f_{mn}=f_m f_n coprime
for p in (2,5,7,11):
    print(f"  p={p}: f_p={sp.simplify(f[p])} ; f_p^2 - f_(p^2) - p^7 = {sp.simplify(f[p]**2 - f[p*p] - p**7) if p*p<=N else 'n/a'}")
print("  multiplicativity f_2 f_5 - f_10 =", sp.simplify(f[2]*f[5]-f[10]), "| f_2 f_7 - f_14 =", sp.simplify(f[2]*f[7]-f[14]), "| f_4 f_5 - f_20 =", sp.simplify(f[4]*f[5]-f[20]))
print("  page's factors: c(2)=6sqrt10:", sp.simplify(f[2]-6*r10)==0, " c(5)=-96sqrt10:", sp.simplify(f[5]+96*r10)==0, " c(7)=260:", sp.simplify(f[7]-260)==0, " c(11)=-1920sqrt10:", sp.simplify(f[11]+1920*r10)==0)

print("== p.72 transformation, case s=2: (1/2) sqrt(x/pi) e^{-2 pi zeta(-1/2)/sqrt(x)} prod(1-e^{-pi n^2 x}) == prod_l {1 - 2 e^{-2 pi sqrt(l/x)} cos(2 pi sqrt(l/x)) + e^{-4 pi sqrt(l/x)}} ?")
for x in (mpf('0.7'), mpf('1.3'), mpf('2.0')):
    L = mpf(1)/2*sqrt(x/pi)*exp(-2*pi*zeta(-mpf(1)/2)/sqrt(x))*nprod(lambda n: 1-exp(-pi*n**2*x), [1,inf])
    R = nprod(lambda l: 1-2*exp(-2*pi*sqrt(l/x))*cos(2*pi*sqrt(l/x))+exp(-4*pi*sqrt(l/x)), [1,inf])
    print(f"  x={x}: LHS={L}  RHS={R}  ratio={L/R}")
print("== s=1 (Dedekind eta) sanity:", end=' ')
x=mpf('0.9'); L=sqrt(x)*exp(-pi*x/12)*nprod(lambda n:1-exp(-2*pi*n*x),[1,inf]); R=exp(-pi/(12*x))*nprod(lambda n:1-exp(-2*pi*n/x),[1,inf]); print(L/R)
