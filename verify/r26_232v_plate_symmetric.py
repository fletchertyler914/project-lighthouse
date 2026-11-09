"""Cod. Ms. B. Riemann 26 fol. 232v (pencil): the companion of fol. 228r - the same exact plate problem for the
modes that are symmetric about the middle plane (cos sigma z instead of sin sigma z).

Page (as read on the scan; struck text omitted):
  p = cos(sigma z) lambda
  u = cos(sigma z) lambda_x + cos(tau z) a tau lambda_x        (v likewise with lambda_y)
  w = -sin(sigma z) sigma lambda + ...                           (shear part struck through and rewritten)
  2(1+theta) cos(sigma z)(lambda_xx + lambda_yy - sigma^2 lambda) + m lambda cos(sigma z)      [= 0]
  cos(tau z)(lambda_xx + lambda_yy - tau^2 lambda) + m lambda cos(tau z)                       [= 0]
  m/(2(1+theta)) - sigma^2 = m - tau^2 = rho
  (-2 sigma^2 -/+ 2 theta rho - 2 theta sigma^2) lambda cos(sigma z) + 2 tau rho cos(tau z) tau a = 0
  sin(sigma z) 2 sigma + a sin(tau z)(tau^2 - rho)                                             [= 0]
  cot(sigma c)(-m - 2 theta rho) ... 4 sigma tau/(m - 2 rho) rho cot(tau c)
  tau^2 - sigma^2 = (1+2 theta)/(2(1+theta)) m ;  c(tau+sigma) = lambda_1, c(tau-sigma) = lambda_2

Checks (sympy): the ansatz solves the elastodynamic equations with exactly the page's two relations for
sigma, tau; the face conditions; the resulting frequency equation and its identity with the symmetric
Rayleigh-Lamb equation; and which factor on the page is a slip.
Run: python3 -E -P verify/r26_232v_plate_symmetric.py
"""
import sympy as sp

x, y, z, c, sg, ta, a, rho, th, mu, m = sp.symbols("x y z c sigma tau a rho theta mu m", positive=True)
lam = sp.cos(sp.sqrt(rho) * x)                       # any lambda with lambda_xx + lambda_yy = -rho lambda
u = (sp.cos(sg * z) + a * ta * sp.cos(ta * z)) * lam.diff(x)
v = (sp.cos(sg * z) + a * ta * sp.cos(ta * z)) * lam.diff(y)
w = -sg * sp.sin(sg * z) * lam + a * rho * sp.sin(ta * z) * lam
U = [u, v, w]
lap = lambda f: f.diff(x, 2) + f.diff(y, 2) + f.diff(z, 2)
div = sp.simplify(u.diff(x) + v.diff(y) + w.diff(z))
print("shear part divergence-free (div independent of a):", sp.simplify(div.diff(a)) == 0)

# equations of motion mu*Lap(U) + (lam_L+mu) grad div U + dens*omega^2 U = 0 with lam_L = 2 mu theta, m = dens*omega^2/mu
X = [x, y, z]
res = [sp.simplify(lap(U[i]) + (2 * th + 1) * div.diff(X[i]) + m * U[i]) for i in range(3)]
sub = {sg: sp.sqrt(m / (2 * (1 + th)) - rho), ta: sp.sqrt(m - rho)}
print("equations of motion hold when m/(2(1+theta)) - sigma^2 = m - tau^2 = rho (the page's line):",
      all(sp.simplify(r.subs(sub)) == 0 for r in res))
print("page: tau^2 - sigma^2 = (1+2 theta)/(2(1+theta)) m:",
      sp.simplify((ta**2 - sg**2).subs(sub) - (1 + 2 * th) / (2 * (1 + th)) * m) == 0)

# face conditions at z = c
szz = sp.simplify((2 * mu * th * div + 2 * mu * w.diff(z)).subs(z, c) / (mu * lam))
sxz = sp.simplify((mu * (u.diff(z) + w.diff(x))).subs(z, c) / (mu * lam.diff(x)))
eq1_right = (-2 * sg**2 - 2 * th * rho - 2 * th * sg**2) * sp.cos(sg * c) + 2 * ta * rho * a * sp.cos(ta * c)
eq2_page = -(2 * sg * sp.sin(sg * c) + a * (ta**2 - rho) * sp.sin(ta * c))
print("normal stress on the face = (-2 sigma^2 - 2 theta rho - 2 theta sigma^2) cos(sigma c) + 2 tau rho a cos(tau c):",
      sp.simplify(szz - eq1_right) == 0)
print("shear stress on the face = -(2 sigma sin(sigma c) + a (tau^2 - rho) sin(tau c)) (page's second condition):",
      sp.simplify(sxz - eq2_page) == 0)
factor = sp.simplify((-2 * sg**2 - 2 * th * rho - 2 * th * sg**2).subs(sub))
print("normal-stress factor in terms of m, rho:", factor, "| page writes (-m - 2 theta rho); correct is -(m - 2 rho):",
      sp.simplify(factor + (m - 2 * rho)) == 0)

# frequency equation
a1 = sp.solve(eq1_right, a)[0]
a2 = sp.solve(eq2_page, a)[0]
chk = sp.simplify((a1 - a2) * (2 * ta * rho * sp.cos(ta * c)) * (ta**2 - rho) * sp.sin(ta * c)
                  - ((2 * sg**2 * (1 + th) + 2 * th * rho) * sp.cos(sg * c) * (ta**2 - rho) * sp.sin(ta * c)
                     + 2 * sg * sp.sin(sg * c) * 2 * ta * rho * sp.cos(ta * c)))
print("elimination of a is consistent:", chk == 0)
lhs = (2 * sg**2 * (1 + th) + 2 * th * rho)
print("with sigma, tau as above, 2 sigma^2(1+theta) + 2 theta rho = tau^2 - rho = m - 2 rho:",
      sp.simplify(lhs.subs(sub) - (m - 2 * rho)) == 0, sp.simplify((ta**2 - rho).subs(sub) - (m - 2 * rho)) == 0)
print("=> frequency equation: cot(sigma c)/cot(tau c) = -4 sigma tau rho/(m - 2 rho)^2, i.e. tan(tau c)/tan(sigma c) = "
      "-4 k^2 p q/(q^2 - k^2)^2 with p = sigma, q = tau, k^2 = rho: the symmetric Rayleigh-Lamb equation.")
print("   page: cot(sigma c)(-m - 2 theta rho) ... 4 sigma tau rho/(m - 2 rho) cot(tau c): same structure, one factor wrong "
      "(m + 2 theta rho written for m - 2 rho).")
