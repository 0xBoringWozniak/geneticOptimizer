from numpy import sin, cos, tan,\
				arcsin, arccos, arctan, arctan2,\
				sinh, cosh, tanh,\
				arcsinh, arccosh, arctanh,\
				exp, expm1, exp2,\
				log, log2, log10, log1p




class Func:
	def __init__(self, to_exec):
		to_exec = to_exec.strip()
		exec('self.f = lambda x, y: ' + to_exec)
	def __call__(self, x, y):
		return self.f(x, y)