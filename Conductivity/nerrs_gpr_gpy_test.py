import numpy as np
from IPython.display import display

GPy.plotting.change_plotting_library('plotly')
X = np.random.uniform(-3.,3.,(20,1))
Y = np.sin(X) + np.random.randn(20,1)*0.05

kernel = GPy.kern.RBF(input_dim=1, variance=1., lengthscale=1.)

GPy.kern.BasisFuncKernel
m = GPy.models.GPRegression(X,Y,kernel)


display(m)
fig = m.plot()
GPy.plotting.show(fig, filename='basic_gp_regression_notebook')
