"""Exact check of arctan relations transcribed from Riemann, Cod. Ms. B. Riemann 27, Bl. 14v.
Notation on the page: (1/n) = arctan(1/n). sum k_j*arctan(1/n_j) == arctan(1/a)
iff  prod (n_j + i)^k_j * conj(a + i)  is a POSITIVE real Gaussian integer."""
import math
def gmul(x, y): return (x[0]*y[0]-x[1]*y[1], x[0]*y[1]+x[1]*y[0])
def gpow(z, k):
    r = (1, 0); b = z if k > 0 else (z[0], -z[1])
    for _ in range(abs(k)): r = gmul(r, b)
    return r
def check(lhs, terms):
    p = (1, 0)
    for k, n in terms: p = gmul(p, gpow((n, 1), k))
    p = gmul(p, (lhs, -1))
    exact = p[1] == 0 and p[0] > 0
    num = abs(math.atan(1/lhs) - sum(k*math.atan(1/n) for k, n in terms))
    return exact, num
REL = [  # (lhs a, [(coef, n), ...])  as read off the page
 (1, [(1,2),(1,3)]), (1, [(2,3),(1,7)]), (1, [(2,5),(1,7),(2,8)]),
 (1, [(3,7),(2,8),(2,18)]), (1, [(5,7),(2,18),(-2,57)]),
 (2, [(1,3),(1,7)]), (3, [(1,5),(1,8)]), (3, [(1,4),(1,13)]), (5, [(1,7),(1,18)]),
 (7, [(1,8),(1,57)]), (12, [(1,17),(1,41)]), (41, [(1,70),(1,99)]), (70, [(1,99),(1,239)]),
 (17, [(1,18),(1,307)]), (57, [(1,70),(1,307)]), (307, [(1,597),(1,632)]),
 (31, [(1,57),(1,68)]), (32, [(1,57),(1,73)]), (17, [(1,22),(1,75)]), (18, [(1,23),(1,83)]),
 (18, [(1,31),(1,43)]), (31, [(1,44),(1,105)]), (43, [(1,68),(1,117)]),
 (68, [(1,93),(1,253)]), (68, [(1,105),(1,193)]), (57, [(1,122),(1,107)]),
 (46, [(1,75),(1,119)]), (57, [(1,47),(-1,268)]), (37, [(1,47),(1,174)]), (17, [(1,27),(1,46)]),
]
ok = 0
for a, t in REL:
    e, num = check(a, t)
    ok += e
    rhs = " + ".join(f"{k}*(1/{n})" for k, n in t).replace("+ -", "- ")
    print(f"{'PASS' if e else 'FAIL'}  (1/{a}) = {rhs:42}  |num diff| = {num:.1e}")
print(f"\narctan relations: {ok}/{len(REL)} exact")
F = [(46,29*73),(27,73*10),(57,13*250),(47,10*13*17),(268,221*325),(157,2*17*29*25),
     (68,25*185),(117,5*37*74),(191,493*74),(93,346*25),(239,2*13**4),(70,13*13*29),(307,290*325)]
fo = sum(n*n+1 == v for n, v in F)
for n, v in F: print(f"{'PASS' if n*n+1==v else 'FAIL'}  {n}^2+1 = {n*n+1}  vs page {v}")
print(f"factorizations: {fo}/{len(F)} exact")
