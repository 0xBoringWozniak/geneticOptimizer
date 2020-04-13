import sys, os
sys.path.append(os.path.abspath('../'))

from function import Func
from optimizer import OptimizerGA





f_x_y = '(x ** 1/2 - 5 * y ) / (x ** 2 + y ** 2  - 2 * x + 10)'

f = Func(f_x_y)
opt = OptimizerGA(f)
opt.startGA(chromosomes_number=8, generations_number=20, mutation=True, optimizer='max')
