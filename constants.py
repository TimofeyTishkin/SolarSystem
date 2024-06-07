import math

g = 6.6743 * 10 ** (-11)
mass = 1.0243*10**26
a = 4503443661000
e = 0.011214269
print(math.sqrt(g*(mass+1.98847 * 10 ** 30)*a*(1-e**2)))
print(e*g*(mass+1.98847 * 10 ** 30)/math.sqrt(g*(mass+1.98847 * 10 ** 30)*a*(1-e**2)))

