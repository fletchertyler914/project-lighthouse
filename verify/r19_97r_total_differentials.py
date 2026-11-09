"""Cod. Ms. Riemann 19 fol. 97r-97v: 1-forms on an algebraic surface f(x,y,z)=0.
Page claims (as read): with a vector field V=(xi,eta,zeta) satisfying xi f_x + eta f_y + zeta f_z = f*rho,
  (i)  (-eta dx + xi dy)/f_z = (eta dz - zeta dy)/f_x = (zeta dx - xi dz)/f_y   on f=0;
  (ii) this 1-form is a 'vollstaendiges Differential' (closed) on f=0  iff  div V = rho  on f=0.
Check symbolically with generic polynomial data: V = f*W + grad f x U  (so V.grad f = f * (W.grad f), rho = W.grad f)."""
import random
import sympy as sp
x, y, z = sp.symbols('x y z')
random.seed(3)
def rp(deg):
    return sum(random.randint(-3, 3) * x**i * y**j * z**k for i in range(deg+1) for j in range(deg+1-i) for k in range(deg+1-i-j))
f = rp(3)
W = sp.Matrix([rp(1), rp(1), rp(1)]); U = sp.Matrix([rp(1), rp(1), rp(1)])
g = sp.Matrix([f.diff(x), f.diff(y), f.diff(z)])
V = f * W + g.cross(U)
xi, eta, zeta = V
rho = sp.expand((W.T * g)[0])
assert sp.expand((V.T * g)[0] - f * rho) == 0
def in_ideal(e):
    return sp.reduced(sp.expand(e), [f], x, y, z)[1] == 0
# (i) the three expressions agree on f=0: compare coefficients of dx, dy after eliminating dz = -(f_x dx + f_y dy)/f_z
fx, fy, fz = g
# form A = (-eta dx + xi dy)/fz ; form B = (eta dz - zeta dy)/fx with dz substituted; compare fz*fx*(A-B) coefficients
A_dx, A_dy = -eta * fx, xi * fx                       # times fx*fz
B_dx, B_dy = eta * (-fx) , eta * (-fy) - zeta * fz    # times fx*fz  (from (eta dz - zeta dy)/fx)
assert in_ideal(A_dx - B_dx) and in_ideal(A_dy - B_dy), "forms (A) and (B) differ on f=0"
C_dx, C_dy = zeta * fz - xi * (-fx), -xi * (-fy)      # (zeta dx - xi dz)/fy times fy*fz ... compare with A times fy*fz
assert in_ideal(fy * (-eta) - (zeta * fz + xi * fx)) and in_ideal(fy * xi - xi * fy)
# (ii) closedness on the surface: P dx + Q dy with P=-eta/fz, Q=xi/fz, total derivatives D_x = d/dx - (fx/fz) d/dz
P, Q = -eta / fz, xi / fz
Dx = lambda h: h.diff(x) - (fx / fz) * h.diff(z)
Dy = lambda h: h.diff(y) - (fy / fz) * h.diff(z)
closed = sp.together(Dx(Q) - Dy(P))
num, den = sp.fraction(closed)
target = sp.expand(xi.diff(x) + eta.diff(y) + zeta.diff(z) - rho)
# Residue argument: omega = Res( (iota_V vol)/f ), so d omega = Res( (div V - rho) vol / f ) = (div V - rho) dx^dy / f_z on f=0.
# Hence  num/den == s*(div V - rho)/f_z  (mod f)  for s = +1 or -1, i.e.  num*f_z - s*den*target  is in the ideal (f).
ok = [s for s in (1, -1) if in_ideal(num * fz - s * den * target)]
print("closedness expression == (div V - rho)/f_z on f=0 (up to sign):", bool(ok), "sign", ok)
# and the converse direction is automatic (same identity). Also check that closedness FAILS when div V != rho: perturb V by a non-divergence-free tangent field.
V2 = V + g.cross(sp.Matrix([x*y, 0, 0]))          # still tangent (V2.grad f = f*rho), div changes by div(grad f x (xy,0,0)) = -(curl(xy,0,0)).grad f
xi2, eta2, zeta2 = V2
P2, Q2 = -eta2 / fz, xi2 / fz
n2, d2 = sp.fraction(sp.together(Dx(Q2) - Dy(P2)))
print("perturbed field still closed?", in_ideal(n2), "(expected False unless the perturbation is divergence-free on f=0)")
