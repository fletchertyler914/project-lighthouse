"""Cod. Ms. Riemann 26 fol. 228r: free flexural vibrations of an elastic plate |z|<=c from 3-D elasticity.
Page (as transcribed):
  p = sin(sigma z) lambda ;  u = (sin sigma z + a tau sin tau z) lambda_x ; v = (...) lambda_y ;
  w = sigma cos(sigma z) lambda - a rho cos(tau z) lambda ;
  boundary eqs:  (-sigma^2 - rho theta - sigma^2 theta) sin(sigma c) + a tau rho sin(tau c) = 0
                 2 sigma cos(sigma c) + a (tau^2 - rho) cos(tau c) = 0
  ratio:  sin(tau c)cos(sigma c)/(sin(sigma c)cos(tau c)) = (tau'^2-rho')[sigma'^2(1+theta)-rho' theta]/(2 sigma' tau' rho')
Check: with Delta_2 lambda = -rho lambda and Kirchhoff's theta = lambda_L/(2 mu): traction-free conditions at z=c
give exactly the two equations; eliminating a gives the Rayleigh-Lamb antisymmetric frequency equation; compare
with the page's ratio formula (model noted a possible sign slip)."""
import sympy as sp
x, y, z, c, sg, ta, a, rho, th, mu, om = sp.symbols('x y z c sigma tau a rho theta mu omega', positive=True)
k = sp.sqrt(rho)
lam = sp.cos(k*x)*sp.cos(0*y)   # concrete plane amplitude with Delta_2 lam = -rho lam
u = (sp.sin(sg*z) + a*ta*sp.sin(ta*z)) * lam.diff(x)
v = (sp.sin(sg*z) + a*ta*sp.sin(ta*z)) * lam.diff(y)
w = sg*sp.cos(sg*z)*lam - a*rho*sp.cos(ta*z)*lam
assert sp.simplify(lam.diff(x,2)+lam.diff(y,2)+rho*lam) == 0
div = sp.simplify(u.diff(x) + v.diff(y) + w.diff(z))
print("div u (should be dilatational part only, i.e. independent of a):", sp.simplify(div))
assert sp.simplify(div.diff(a)) == 0
# Lame constants: lambda_L = 2 mu theta.  sigma_zz = lambda_L div + 2 mu w_z ; sigma_xz = mu (u_z + w_x)
szz = (2*mu*th*div + 2*mu*w.diff(z)).subs(z, c)
sxz = (mu*(u.diff(z) + w.diff(x))).subs(z, c)
eq1_page = (-sg**2 - rho*th - sg**2*th)*sp.sin(sg*c) + a*ta*rho*sp.sin(ta*c)
eq2_page = 2*sg*sp.cos(sg*c) + a*(ta**2 - rho)*sp.cos(ta*c)
r1 = sp.simplify(szz/(2*mu*lam) - eq1_page)
r2 = sp.simplify(sxz/(mu*lam.diff(x)) - eq2_page)
print("sigma_zz/(2 mu lam) - page eq1 =", r1)
print("sigma_xz/(mu lam_x) - page eq2 =", r2)
# eliminate a: frequency equation
a1 = sp.solve(eq1_page, a)[0]; a2 = sp.solve(eq2_page, a)[0]
freq = sp.simplify(a1 - a2)
ratio_lhs = sp.sin(ta*c)*sp.cos(sg*c)/(sp.sin(sg*c)*sp.cos(ta*c))
# from eq1: a = (sg^2(1+th)+rho th) sin(sg c)/(ta rho sin(ta c)); from eq2: a = -2 sg cos(sg c)/((ta^2-rho) cos(ta c))
# => sin(ta c)cos(sg c)/(sin(sg c)cos(ta c)) = -(ta^2-rho)(sg^2(1+th)+rho th)/(2 sg ta rho)
ours = -(ta**2 - rho)*(sg**2*(1+th) + rho*th)/(2*sg*ta*rho)
page = (ta**2 - rho)*(sg**2*(1+th) - rho*th)/(2*sg*ta*rho)
print("derived ratio:", ours, "| page ratio:", page)
print("page == derived?", sp.simplify(ours - page) == 0, "| page == -derived with +rho th?", sp.simplify(ours + (ta**2-rho)*(sg**2*(1+th)+rho*th)/(2*sg*ta*rho)) == 0)
# Rayleigh-Lamb antisymmetric equation (Graff / Achenbach form): tan(q h)/tan(p h) = -(k^2-q^2)^2/(4 k^2 p q)  with p^2 = w^2/cL^2 - k^2 (=sigma^2), q^2 = w^2/cT^2 - k^2 (=tau^2), k^2 = rho.
# Using sigma^2 + rho = kL^2, tau^2 + rho = kT^2, kT^2/kL^2 = 2(1+theta):  sg^2(1+th)+rho th = ((tau^2+rho)/2 - rho) ... check numerically below
kL2 = sg**2 + rho; kT2 = ta**2 + rho
th_val = sp.solve(sp.Eq(kT2/kL2, 2*(1+th)), th)[0]
RL = -(rho - ta**2)**2/(4*rho*sg*ta)      # tan(tau c)/tan(sigma c) per Rayleigh-Lamb (antisymmetric)
ours_th = ours.subs(th, th_val)
print("derived == Rayleigh-Lamb antisymmetric form?", sp.simplify(ours_th - RL) == 0)
