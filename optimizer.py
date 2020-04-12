import numpy as np
import numpy.random as rd
from accessify import protected

from collections import OrderedDict

import function


class OptimizerGA:
	def __init__(self, function):
		self.chromosomes = np.array([])
		self.function = function

	@protected
	def generate_new_part(self, chromosomes, mutation=False, optimizer='min'):
		values = [self.function(*chromosome) for chromosome in chromosomes]
		chromosomesDict = dict(zip([str(i) for i in range(4)], values))

		if optimizer == 'min':
			chromosomesDict = OrderedDict(sorted(chromosomesDict.items(), key=lambda t: t[1]))
		elif optimizer == 'max':
			chromosomesDict = OrderedDict(sorted(chromosomesDict.items(), key=lambda t: -t[1]))
		else:
			raise ValueError(str(optimizer) + 'should be max or min')

		chromosome_indexes = list()

		for chromosome_index in chromosomesDict.keys():
			chromosome_indexes.append(chromosome_index)

		good_chromosome = chromosomes[int(chromosome_indexes[2])]
		better_chromosome = chromosomes[int(chromosome_indexes[1])]
		best_chromosome = chromosomes[int(chromosome_indexes[0])]

		new_part = np.array([	[better_chromosome[0], best_chromosome[1] + float(mutation * rd.rand(1))],
								[good_chromosome[0] + float(mutation * rd.rand(1)), best_chromosome[1]],
								[best_chromosome[0], better_chromosome[0] + float(mutation * rd.rand(1))],
								[best_chromosome[0], good_chromosome[1]] ])
		return new_part

	def next_generation(self, mutation=False, optimizer='min'):
		part = np.array([self.chromosomes[j] for j in range(0 , 4)])
		new_population = self.generate_new_part(part, mutation, optimizer)

		for parts_number in range(1, int(len(self.chromosomes) / 4)):
			part = np.array([self.chromosomes[j] for j in range(parts_number * 4, (parts_number + 1) * 4)])
			new_part = self.generate_new_part(part, mutation, optimizer)
			new_population = np.append(new_population, new_part, axis=0)

		return new_population

	@protected
	def calculate(self, optimizer='min'):
		if optimizer == 'min':
			return min([self.function(*chromosome) for chromosome in self.chromosomes])
		elif optimizer == 'max':
			return max([self.function(*chromosome) for chromosome in self.chromosomes])
		else:
			raise ValueError(optimizer + 'should be max or min')

	@protected
	def startGA(self, chromosoms_number=4, generations_number=10, mutation=False, optimizer='min'):
		self.chromosomes = np.array([(chromosoms_number * rd.rand(2) - (chromosoms_number / 2)) for i in range(chromosoms_number)])
		for i in range(generations_number):
			self.chromosomes = self.next_generation(mutation, optimizer)
			print('generation {} :\n {}'.format(i, self.chromosomes))

	def startGA_with_statistics(self, chromosoms_number=4, generations_number=10, mutation=False, optimizer='min'):
		self.chromosomes = np.array([(chromosoms_number * rd.rand(2) - (chromosoms_number / 2)) for i in range(chromosoms_number)])
		with open('GA-statistics.txt', 'w') as f:
			if optimizer == 'min':
				for i in range(generations_number):
					self.chromosomes = self.next_generation(mutation, optimizer)
					f.write('_' * 70)
					f.write('\nINFO about generation {}:\n'.format(i))
					for chromosome in self.chromosomes:
						f.write('chromosome {} gives value: {}\n'.format(chromosome, self.function(*chromosome)))
					f.write('min value for this generation: {}\n'.format(self.calculate(optimizer)))
			elif optimizer == 'max':
				f.write('_' * 70)
				for i in range(generations_number):
					self.chromosomes = self.next_generation(mutation, optimizer)
					f.write('\nINFO about generation {}:\n'.format(i))
					for chromosome in self.chromosomes:
						f.write('chromosome {} gives value: {}\n'.format(chromosome, self.function(*chromosome)))
					f.write('max value for this generation: {}\n'.format(self.calculate(optimizer)))
			else:
				raise ValueError(optimizer + 'should be max or min')

