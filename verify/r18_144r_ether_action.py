"""Cod. Ms. B. Riemann 18 fol. 144r (pencil): a joint action for a charged mass point and an elastic medium.

Page (as read on the scan):
  m Sum(dx/dt)^2 + 2 eps Sum (dx/dt) xi + a Sum(d xi/dt)^2 + b Sum(d xi/dx)^2 + (c-b)(div xi)^2 = 2(T + U)
  Int (T + U) dt = Min.
  a xi_tt = b Sum xi_xx + (c-b) d(div xi)/dx - eps dx/(dt dS)
  m x'' + eps( xi_t + Sum_i (d xi/dx_i - d xi_i/dx) x_i' ) - ...
Checks (sympy): the particle line is the Euler-Lagrange equation of L = m v^2/2 + eps v.xi + U and equals
m x'' = eps(-xi_t + v x curl xi) + grad U; which sign pattern of the medium terms reproduces the page's wave
equation and source sign; the case c = 0 (Maxwell's equations with zero scalar potential); the lower half as a
Gauss least-constraint function. Written by an independent reviewer from the scan, 2026-11-09.
Run: python3 -E -P verify/r18_144r_ether_action.py
"""
import sympy as sp
from sympy.calculus.euler import euler_equations

t = sp.symbols('t', real=True)
m, eps, a, b, c = sp.symbols('m epsilon a b c', real=True)
X = [sp.Function('x%d' % i)(t) for i in (1, 2, 3)]          # particle coordinates
xs = sp.symbols('X1 X2 X3', real=True)                         # field point
xi_f = [sp.Function('xi%d' % i) for i in (1, 2, 3)]            # medium vector (xi, eta, zeta)
U_f = sp.Function('U')

# ---------- 1. particle equation ----------
xi_at = [f(*X, t) for f in xi_f]
V = [sp.diff(x, t) for x in X]
Lp = sp.Rational(1, 2)*m*sum(v**2 for v in V) + eps*sum(v*q for v, q in zip(V, xi_at)) + U_f(*X)
EL = [sp.diff(sp.diff(Lp, V[k]), t) - sp.diff(Lp, X[k]) for k in range(3)]   # = 0

# modern form: m x'' = eps(-d_t xi + v x curl xi) + grad U
def d(expr_f, j):      # partial derivative of field component wrt j-th slot (0..2 space, 3 time), at particle
    args = list(xs) + [sp.Symbol('T')]
    e = sp.diff(expr_f(*args), args[j])
    return e.subs(dict(zip(args, X + [t])), simultaneous=True)
def dd(f, j):
    args = list(xs) + [sp.Symbol('T')]
    return sp.diff(f(*args), args[j]).subs(dict(zip(args, X + [t])), simultaneous=True)
curl = [dd(xi_f[2], 1) - dd(xi_f[1], 2), dd(xi_f[0], 2) - dd(xi_f[2], 0), dd(xi_f[1], 0) - dd(xi_f[0], 1)]
vxc = [V[1]*curl[2] - V[2]*curl[1], V[2]*curl[0] - V[0]*curl[2], V[0]*curl[1] - V[1]*curl[0]]
Ua = sp.Function('U')(*xs)
gradU = [sp.diff(Ua, xs[k]).subs(dict(zip(xs, X)), simultaneous=True) for k in range(3)]
ok1 = []
for k in range(3):
    modern = m*sp.diff(X[k], t, 2) - eps*(-dd(xi_f[k], 3) + vxc[k]) - gradU[k]
    ok1.append(sp.simplify((EL[k] - modern).doit()) == 0)
print('1a. EL(particle) == m x" - eps(-d_t xi + v x curl xi) - grad U :', ok1)

# the page's line: m x" + eps( d_t xi + sum_i (d xi/d x_i - d xi_i/d x) x_i' ) - dU/dx = 0
ok2 = []
for k in range(3):
    page = m*sp.diff(X[k], t, 2) + eps*(dd(xi_f[k], 3) + sum((dd(xi_f[k], i) - dd(xi_f[i], k))*V[i] for i in range(3))) - gradU[k]
    ok2.append(sp.simplify((EL[k] - page).doit()) == 0)
print('1b. EL(particle) == page line (below the rule)                  :', ok2)
# the page's line above the rule: d/dt(m x' + eps xi) = eps sum_i (d xi_i/dx) x_i' + dU/dx
ok3 = []
for k in range(3):
    lhs = sp.diff(m*V[k] + eps*xi_at[k], t)
    rhs = eps*sum(dd(xi_f[i], k)*V[i] for i in range(3)) + gradU[k]
    ok3.append(sp.simplify((EL[k] - (lhs - rhs)).doit()) == 0)
print('1c. EL(particle) == page line (above the rule, canonical momentum m x\'+eps xi):', ok3)

# ---------- 2. field equation ----------
T_ = sp.symbols('T', real=True)
F = [f(*xs, T_) for f in xi_f]
J = [sp.Function('j%d' % i)(*xs, T_) for i in (1, 2, 3)]       # eps * velocity * delta = current density
div = sum(sp.diff(F[i], xs[i]) for i in range(3))
def dens(sa, sb, sc):
    return (sp.Rational(1, 2)*(sa*a*sum(sp.diff(q, T_)**2 for q in F)
                               + sb*b*sum(sp.diff(F[i], xs[j])**2 for i in range(3) for j in range(3))
                               + sc*(c - b)*div**2)
            + sum(J[i]*F[i] for i in range(3)))
lap = lambda q: sum(sp.diff(q, x, 2) for x in xs)
for (sa, sb, sc, name) in [(1, -1, -1, 'kinetic +a, elastic -b, -(c-b)  [mechanically natural]'),
                           (1, 1, 1, 'all plus, as the top line now stands'),
                           (-1, 1, 1, '-a, +b, +(c-b)')]:
    eqs = euler_equations(dens(sa, sb, sc), F, list(xs) + [T_])
    res = []
    for k in range(3):
        # solve for a*xi_tt
        expr = eqs[k].lhs - eqs[k].rhs
        sol = sp.solve(expr, sp.diff(F[k], T_, 2))[0]*a
        natural = b*lap(F[k]) + (c - b)*sp.diff(div, xs[k])
        res.append((sp.simplify(sol - (natural + J[k])) == 0, sp.simplify(sol - (natural - J[k])) == 0,
                    sp.simplify(sol - (-natural + J[k])) == 0))
    print('2.', name, '\n    a xi_tt = b Lap xi + (c-b) grad div xi + j :', [r[0] for r in res],
          '\n    a xi_tt = b Lap xi + (c-b) grad div xi - j :', [r[1] for r in res],
          '\n    a xi_tt = -b Lap xi - (c-b) grad div xi + j:', [r[2] for r in res])

# ---------- 3. identity: b Lap xi + (c-b) grad div xi = -b curl curl xi + c grad div xi ----------
def curlv(Fv):
    return [sp.diff(Fv[2], xs[1]) - sp.diff(Fv[1], xs[2]), sp.diff(Fv[0], xs[2]) - sp.diff(Fv[2], xs[0]),
            sp.diff(Fv[1], xs[0]) - sp.diff(Fv[0], xs[1])]
cc = curlv(curlv(F))
print('3. b Lap + (c-b) grad div == -b curl curl + c grad div :',
      [sp.simplify(b*lap(F[k]) + (c - b)*sp.diff(div, xs[k]) - (-b*cc[k] + c*sp.diff(div, xs[k]))) == 0 for k in range(3)])

# ---------- 4. c = 0: Maxwell in temporal gauge. E = -xi_t, B = curl xi ----------
# field eq (natural sign): a xi_tt + b curl curl xi = j  <=>  curl B = j/b + (a/b) dE/dt
E = [-sp.diff(q, T_) for q in F]; B = curlv(F)
amp = [sp.simplify((a*sp.diff(F[k], T_, 2) + b*cc[k] - J[k]) - b*(curlv(B)[k] - J[k]/b - (a/b)*sp.diff(E[k], T_))) == 0 for k in range(3)]
far = [sp.simplify(curlv(E)[k] + sp.diff(B[k], T_)) == 0 for k in range(3)]
divB = sp.simplify(sum(sp.diff(B[i], xs[i]) for i in range(3))) == 0
# divergence of field eq: a d_t^2 div xi = div j  -> d_t( a div E + rho ) = 0 if d_t rho + div j = 0
lhs = sum(sp.diff(a*sp.diff(F[k], T_, 2) + b*cc[k] - J[k], xs[k]) for k in range(3))
gauss = sp.simplify(lhs - (-sp.diff(a*sum(sp.diff(E[i], xs[i]) for i in range(3)), T_) - sum(sp.diff(J[i], xs[i]) for i in range(3)))) == 0
print('4. c=0: Ampere-Maxwell form', amp, '| Faraday identity', far, '| div B = 0', divB,
      '| div(field eq) = -d_t(a div E) - div j', gauss)

# ---------- 5. Gauss-type (least constraint) function in the accelerations ----------
A = sp.symbols('A1 A2 A3', real=True)   # accelerations treated as free
Fk = [eps*(-dd(xi_f[k], 3) + vxc[k]) for k in range(3)]
Z = sum(m*A[k]**2 - 2*Fk[k]*A[k] for k in range(3))     # page: m x"^2 + 2 eps( d_t xi + sum(..)x') x"
stat = [sp.simplify(sp.diff(Z, A[k])/2 - (m*A[k] - Fk[k])) == 0 for k in range(3)]
print('5. d/dA [ m A^2 + 2 eps(d_t xi + sum(dxi/dx_i - dxi_i/dx) x_i\') A ] = 0 reproduces the particle equation:', stat)
