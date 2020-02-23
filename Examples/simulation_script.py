from FCW_library import FCW_model

L = 100
rho = 0.5

l = 2

t = 10**5

foldername = 'l_%i' % l

model = FCW_model(L, l, rho)

model.simulate(t, folder=foldername)
