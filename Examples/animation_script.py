from FCW_library import *

L = 100
rho = 0.1

l = 5

t = 10**5

model = FCW_model(L, l, rho)

model.animate(t)
