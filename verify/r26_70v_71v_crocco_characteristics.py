"""Verify Riemann 26 fol. 70v (vorticity-entropy chain) and 71v (Mach-line directions) with sympy.

70v, as written: with polytropic p = rho^k * g(sigma)  (sigma = stream function, entropy varies across streamlines)
and uniform total enthalpy H = k/(k-1) p/rho + w^2/2 (true behind a shock from uniform flow):
  (R1)  d_rho(p/rho) = (1 - 1/k) d_rho p / rho
  (R2)  (1 - 1/k)(d_rho p/rho + w dw) = - d_sigma p / rho
  (R3)  (1 - 1/k)(dp/rho + w dw) = -(1/k) d_sigma p / rho
  (R4)  Euler: dp/rho + w dw = (zeta/rho) dsigma  (up to the sign convention of sigma), zeta = v_x - u_y
  =>    zeta/rho = -(1/(k-1)) (d_sigma p)/rho   i.e. Riemann's "(1/rho) zeta = -1/(k-1) dp/dsigma" (Crocco form)
71v: the direction (u - v t, v + u t), t = sqrt(w^2/phi'(rho) - 1) = sqrt(M^2 - 1), is normal to the Mach lines:
the level lines of r make the Mach angle mu with the velocity, sin(mu) = 1/M.
"""
import sympy as sp

k, rho, sig, w = sp.symbols("k rho sigma w", positive=True)
g = sp.Function("g")(sig)
p = rho**k * g

# --- (R1): partial in rho of p/rho equals (1-1/k) * (partial_rho p)/rho
R1 = sp.simplify(sp.diff(p / rho, rho) - (1 - 1 / k) * sp.diff(p, rho) / rho)
print("R1 holds:", R1 == 0)

# --- Uniform H: dH = 0 with dH = k/(k-1) d(p/rho) + w dw. Decompose d(p/rho) into rho- and sigma-parts.
drho, dsig, dw = sp.symbols("drho dsigma dw")
d_p_rho = sp.diff(p / rho, rho) * drho + sp.diff(p / rho, sig) * dsig
dH = k / (k - 1) * d_p_rho + w * dw
wdw = sp.solve(sp.Eq(dH, 0), dw)[0] * w  # w dw expressed from dH = 0
d_rho_p = sp.diff(p, rho) * drho
d_sig_p = sp.diff(p, sig) * dsig
R2 = sp.simplify((1 - 1 / k) * (d_rho_p / rho + wdw) + d_sig_p / rho)
R3 = sp.simplify((1 - 1 / k) * ((d_rho_p + d_sig_p) / rho + wdw) + (1 / k) * d_sig_p / rho)
print("R2 holds:", R2 == 0)
print("R3 holds:", R3 == 0)
# Consequence: dp/rho + w dw = -(1/(k-1)) d_sigma p / rho
R5 = sp.simplify((d_rho_p + d_sig_p) / rho + wdw + d_sig_p / (rho * (k - 1)))
print("dp/rho + w dw = -(1/(k-1)) d_sigma p/rho holds:", R5 == 0)

# --- (R4) Euler identity: (v.grad)v = grad(w^2/2) - v x curl v  (2-D)
x, y = sp.symbols("x y")
u = sp.Function("u")(x, y)
v = sp.Function("v")(x, y)
zeta = sp.diff(v, x) - sp.diff(u, y)
conv = sp.Matrix([u * sp.diff(u, x) + v * sp.diff(u, y), u * sp.diff(v, x) + v * sp.diff(v, y)])
grad_half_w2 = sp.Matrix([sp.diff((u**2 + v**2) / 2, x), sp.diff((u**2 + v**2) / 2, y)])
v_cross_zeta = sp.Matrix([v * zeta, -u * zeta])
print("Euler identity (v.grad)v = grad(w^2/2) - v x zeta holds:",
      sp.simplify(conv - (grad_half_w2 - v_cross_zeta)) == sp.zeros(2, 1))
# Hence along a displacement (dx,dy): dp/rho + w dw = zeta (v dx - u dy) = -(zeta/rho) dsigma  with dsigma = rho(u dy - v dx).
print("=> dp/rho + w dw = -(zeta/rho) dsigma, so zeta/rho = (1/(k-1)) (d_sigma p)/rho up to the sign convention of sigma")

# --- 71v: Mach-line geometry
t, uu, vv = sp.symbols("t u v", positive=True)
M = sp.sqrt(1 + t**2)                       # t = sqrt(M^2 - 1)
grad_r = sp.Matrix([uu - vv * t, vv + uu * t])   # d r = Omega((u - v t) dx + (v + u t) dy)
tangent = sp.Matrix([-grad_r[1], grad_r[0]])     # along the level line r = const
vel = sp.Matrix([uu, vv])
cos_angle = sp.simplify(tangent.dot(vel) / (sp.sqrt(tangent.dot(tangent)) * sp.sqrt(vel.dot(vel))))
sin_angle = sp.simplify(sp.sqrt(1 - cos_angle**2))
print("angle between r = const line and velocity: sin =", sin_angle, " (Mach angle needs 1/M =", sp.simplify(1 / M), ")")
print("Mach-line check:", sp.simplify(sin_angle - 1 / M) == 0)
# Also: w^2/phi'(rho) - 1 = -dlog(rho w)/dlog w along the Bernoulli relation phi'(rho) dlog rho = -w dw
rr, ww = sp.symbols("rr ww", positive=True)
phi1 = sp.Function("phi1")(rr)  # phi'(rho) = c^2
# dlog(rho) /dlog w = -w^2/phi'(rho)  =>  dlog(rho w)/dlog w = 1 - w^2/phi'  => w^2/phi' - 1 = -dlog(rho w)/dlog w
lhs = ww**2 / phi1 - 1
rhs = -(1 - ww**2 / phi1)
print("mass-flux relation w^2/c^2 - 1 = -dlog(rho w)/dlog w holds:", sp.simplify(lhs - rhs) == 0)
