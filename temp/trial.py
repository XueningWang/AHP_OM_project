import sympy as sym

z = sym.symbols('z')
expr = 2*z**2 + 0.1*z**1 + 0.9*z**0
for arg in expr.args:
    for a in arg.args:
        print(a, type(a))
