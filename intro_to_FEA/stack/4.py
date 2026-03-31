from sympy import *

init_printing(use_unicode=True)

E, A, L, rho, omega, m = symbols('E A L rho omega m')

K = Matrix([
    [E*A*L, E*A*L**2, E*A*L**3, E*A*L**4, E*A*L**5],
    [E*A*L**2, 4/3*E*A*L**3, 6/4*E*A*L**4, 8/5*E*A*L**5, 10/6*E*A*L**6],
    [E*A*L**3, 6/4*E*A*L**4, 9/5*E*A*L**5, 12/6*E*A*L**6, 15/7*E*A*L**7],
    [E*A*L**4, 8/5*E*A*L**5, 12/6*E*A*L**6, 16/7*E*A*L**7, 20/8*E*A*L**8],
    [E*A*L**5, 10/6*E*A*L**6, 15/7*E*A*L**7, 20/8*E*A*L**8, 25/9*E*A*L**9],
    ])

F = Matrix([
    rho*omega**2*A*(L**3)/3 + m*omega**2*L**2,
    rho*omega**2*A*(L**4)/4 + m*omega**2*L**3,
    rho*omega**2*A*(L**5)/5 + m*omega**2*L**4,
    rho*omega**2*A*(L**6)/6 + m*omega**2*L**5,
    rho*omega**2*A*(L**7)/7 + m*omega**2*L**6,
    ])

U = (K**-1) * F
pprint(simplify(U)) 