# Riemann Nachlass, Cod. Ms. B. Riemann "Abel'sche Functionen [und Theta]" (HS-3206670) fol. 3v: oblique shock.
from sympy import symbols, simplify, solve, Eq, limit, oo, diff, sqrt
L,u1,u2,A2 = symbols('L u1 u2 A2', positive=True); k = L + 1
# 1) energy-conserving oblique shock (mass, normal momentum, total enthalpy) => L*u_n1*u_n2 = a^2 - w_t^2 (Riemann: aa - bb sin^2 phi = bc cos phi cos psi * lam^2)
expr = A2/(k*u1) + u1*(k-1)/k - (A2/(k*u2) + u2*(k-1)/k)
print("1) normal-shock momentum/energy => L u1 u2 = a^2 - w_t^2:", simplify(expr - (u2-u1)*(A2-L*u1*u2)/((L+1)*u1*u2)) == 0)
x,t,n,s = symbols('x t n s', positive=True)
sol = solve(Eq((n**2-1)*x + n**2/x, L*(1-x*t)/(x+t)), t)[0]
print("2) Riemann's tan(alpha)/x formula:", simplify(sol/x - ((1-n**2/L)-(n**2-1)/L*x**2)/(((n**2-1)/L+1)*x**2+n**2/L)) == 0)
n2 = (s+L)/(1+s)
e1 = ((1-n2/L)-(n2-1)/L*x**2)/(((n2-1)/L+1)*x**2+n2/L); e2 = (s-x**2)*(1-1/L)/((2+s-1/L)*x**2+1+s/L)
print("3) s-parametrised form:", simplify(e1-e2) == 0)
hyp = limit(e2*x, s, oo)
print("4) hypersonic limit s->oo: tan(alpha) =", simplify(hyp), " == (L-1)x/(1+L x^2):", simplify(hyp - (L-1)*x/(1+L*x**2)) == 0)
f = (L-1)*x/(1+L*x**2); xs = solve(diff(f, x), x)[0]; g = (L+1)/(L-1)
print("5) max deflection at x = 1/sqrt(L): sin(alpha_max) = 1/gamma:", simplify(f.subs(x, xs)**2/(1+f.subs(x, xs)**2) - 1/g**2) == 0)
import math; gam = 1.4; print("   for gamma=1.4: alpha_max(M->inf) =", round(math.degrees(math.asin(1/gam)), 2), "deg (textbook: 45.58 deg)")
