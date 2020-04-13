class Func:
	def __init__(self, to_exec):
		to_exec = to_exec.strip()
		exec('self.f = lambda x, y: ' + to_exec)
	def __call__(self, x, y):
		return self.f(x, y)