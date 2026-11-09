# Riemann Nachlass (Cod. Ms. B. Riemann, Mathematische Notizen 1853-63) fol. 70r: shock relations.
# Check that Riemann's written relations follow from mass + momentum + ENERGY conservation (Rankine-Hugoniot),
# and that they are NOT the isentropic (Riemann 1860) jump conditions.
import sympy as sp
k, r1, v1, v2, p1, p2 = sp.symbols('k rho1 v1 v2 p1 p2', positive=True)
m = r1*v1; r2 = m/v2
mom = sp.Eq(p1 - p2, m*(v2 - v1))                                       # written on page
energy = sp.Eq(k/(k-1)*p1/r1 + v1**2/2, k/(k-1)*p2/r2 + v2**2/2)         # total enthalpy conserved
sol = sp.solve([mom, energy], [p1, p2], dict=True)[0]
print("p1+p2 == (1/k) rho1 v1 (v1+v2):", sp.simplify(sol[p1] + sol[p2] - m*(v1+v2)/k) == 0)
print("2p1/(v1 rho1) == v2(1/k+1) - v1(1-1/k):", sp.simplify(2*sol[p1]/m - (v2*(1/k+1) - v1*(1-1/k))) == 0)
print("2p2/(v2 rho2) == v1(1/k+1) - v2(1-1/k):", sp.simplify(2*sol[p2]/(r2*v2) - (v1*(1/k+1) - v2*(1-1/k))) == 0)
lhs2 = 2*sol[p2]/r2 + v2**2*(1-1/k); lhs1 = 2*sol[p1]/r1 + v1**2*(1-1/k)
print("2p2/rho2+v2^2(1-1/k) == v1v2(1+1/k) == 2p1/rho1+v1^2(1-1/k):",
      sp.simplify(lhs2 - v1*v2*(1+1/k)) == 0 and sp.simplify(lhs1 - v1*v2*(1+1/k)) == 0)
# Contrast: isentropic jump (Riemann 1860): p/rho^k continuous instead of energy. Does it satisfy p1+p2=(1/k)m(v1+v2)?
k_, rr1 = sp.Rational(7, 5), 1
import math
# numeric example: Mach 2 shock in air, rho1=1, p1=1
kk = 1.4; M1 = 2.0; c1 = math.sqrt(kk*1/1); V1 = M1*c1
# Rankine-Hugoniot downstream
V2 = V1*((kk-1)*M1**2+2)/((kk+1)*M1**2); P2 = 1*(2*kk*M1**2-(kk-1))/(kk+1)
print("RH example: p1+p2 =", 1+P2, " (1/k)m(v1+v2) =", (1/kk)*1*V1*(V1+V2))
# isentropic + mass + momentum: solve for v2 with p2 = (rho2)^k, rho2 = V1/v2
f = lambda v: (1 - (V1/v)**kk) - V1*(v - V1)
lo, hi = 0.2, V1*0.999
for _ in range(200):
    mid = (lo+hi)/2
    (lo, hi) = (mid, hi) if f(lo)*f(mid) > 0 else (lo, mid)
vi = (lo+hi)/2; pi_ = (V1/vi)**kk
print("isentropic example: p1+p2 =", 1+pi_, " (1/k)m(v1+v2) =", (1/kk)*V1*(V1+vi), "-> relation fails for isentropic jump")
