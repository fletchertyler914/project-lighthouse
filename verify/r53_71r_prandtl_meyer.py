# Riemann Nachlass fol.71r: steady 2-D supersonic flow. Check that Riemann's parametrisation and his invariant
# 2r = sigma + nu(y), nu(y) = lam*atan(y/lam) - atan(y), y = sqrt(M^2-1), lam^2 = (k+1)/(k-1), is the Prandtl-Meyer function.
import sympy as sp
y, lam, a, k, M = sp.symbols('y lam a k M', positive=True)
c2 = a**2/(lam**2 + y**2); w2 = a**2*(1 + y**2)/(lam**2 + y**2)       # Riemann's c^2 and omega^2
print("Bernoulli (lam^2-1)c^2 + w^2 = a^2:", sp.simplify((lam**2-1)*c2 + w2 - a**2) == 0)
print("w^2/c^2 - 1 = y^2 (y = sqrt(M^2-1)):", sp.simplify(w2/c2 - 1 - y**2) == 0)
nu = lam*sp.atan(y/lam) - sp.atan(y)
print("d nu = sqrt(M^2-1) d log w  (characteristic invariant):", sp.simplify(sp.diff(nu, y) - y*sp.diff(sp.log(sp.sqrt(w2)), y)) == 0)
# compare with the textbook Prandtl-Meyer function in terms of M
PM = sp.sqrt((k+1)/(k-1))*sp.atan(sp.sqrt((k-1)/(k+1)*(M**2-1))) - sp.atan(sp.sqrt(M**2-1))
expr = nu.subs({lam: sp.sqrt((k+1)/(k-1)), y: sp.sqrt(M**2-1)}) - PM
print("nu(y) == textbook Prandtl-Meyer nu(M):", sp.simplify(expr) == 0 or abs(sp.N(expr.subs({k: 1.4, M: 2.3}))) < 1e-12)
print("example nu(M=2, k=1.4) degrees:", sp.N(sp.deg(PM.subs({k: sp.Rational(7, 5), M: 2}))))
