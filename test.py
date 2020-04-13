from geneticOptimizer import *

def f(x, y):
	return x + y ** 2

opt1 = OptimizerGA(f)
opt2 = OptimizerGA('x - y ** 2')
opt3 = OptimizerGA(Func('2 * x - y ** 2'))
opt4 = OptimizerGA(lambda x, y: 1 + x + y)