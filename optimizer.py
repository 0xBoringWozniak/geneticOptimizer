import numpy as np
import numpy.random as rd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from accessify import protected
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter
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

		new_part = np.array([	[better_chromosome[0] + float(mutation * rd.rand(1)), best_chromosome[1]],
								[good_chromosome[0]   + float(mutation * rd.rand(1)), best_chromosome[1]],
								[best_chromosome[0], better_chromosome[0] + float(mutation * rd.rand(1))],
								[best_chromosome[0], good_chromosome[1]   + float(mutation * rd.rand(1))]])
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
	def startGA(self, chromosomes_number=4, generations_number=10, mutation=False, optimizer='min'):
		self.chromosomes = np.array([(chromosomes_number * rd.rand(2) - (chromosomes_number / 2)) for i in range(chromosomes_number)])
		for i in range(generations_number):
			self.chromosomes = self.next_generation(mutation, optimizer)
			df = pd.DataFrame(self.chromosomes, columns=['x', 'y'])
			df['f(x, y)'] = self.function(df['x'], df['y'])
			df.to_csv("chromosomes/chromosomes_{}.csv".format(i + 1))

	@protected
	def plotGA(self, chromosomes_number, generations_number, optimizer):
		data = pd.concat([pd.read_csv('chromosomes/chromosomes_{}.csv'.format(i + 1), index_col=0) 
								for i in range(generations_number)], ignore_index=True)

		data['time'] = [i for i in range(chromosomes_number * generations_number)]

		def update_graph(num):
			df = data[abs(num - data['time']) <= chromosomes_number]
			graph.set_data (np.array(df['x']), np.array(df['y']))
			graph.set_3d_properties(np.array(df['f(x, y)']))
			title.set_text('GA-optimizer plot, time={}'.format(num))
			return title, graph, 

		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')


		# Make data.
		X = np.arange(-5, 5, 0.25)
		Y = np.arange(-5, 5, 0.25)
		X, Y = np.meshgrid(X, Y)
		Z = self.function(X, Y)

		if optimizer == 'min':
			color = 'blue'
			color_map = cm.OrRd
		else:
			color = 'red'
			color_map = cm.Blues

		# Plot the surface.
		surf = ax.plot_surface(X, Y, Z, cmap=color_map,
								linewidth=0, antialiased=True)

		title = ax.set_title('GA-optimizer plot')

		df = data[data['time'] == 0]
		graph, = ax.plot(np.array(df['x']), np.array(df['y']), np.array(df['f(x, y)']), 
								linestyle="", c=color, marker='o', ms=5)

		anim = animation.FuncAnimation(fig, update_graph, chromosomes_number * generations_number - 1, interval=chromosomes_number, save_count=True)

		# Customize the z axis.
		ax.set_zlim(-1.31, 1.31)
		ax.zaxis.set_major_locator(LinearLocator(10))
		ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

		ax.set_xlabel('X')
		ax.set_ylabel('Y')
		ax.set_zlabel('Z')

		# Add a color bar which maps values to colors.
		fig.colorbar(surf, shrink=0.8, aspect=3)

		plt.show()
		# anim.save('GA-animation.gif', writer='imagemagick', fps=60)


	def startGA_with_statistics(self, chromosomes_number=4, generations_number=10, mutation=False, optimizer='min'):
		self.startGA(chromosomes_number, generations_number, mutation, optimizer)
		with open('GA-statistics.txt', 'w') as f:
			if optimizer == 'min':
				for i in range(generations_number):
					self.chromosomes = self.next_generation(mutation, optimizer)
					f.write('_' * 70)
					f.write('\nINFO about generation {}:\n'.format(i + 1))
					for chromosome in self.chromosomes:
						f.write('chromosome {} gives value: {}\n'.format(chromosome, self.function(*chromosome)))
					f.write('min value for this generation: {}\n'.format(self.calculate(optimizer)))
			elif optimizer == 'max':
				for i in range(generations_number):
					self.chromosomes = self.next_generation(mutation, optimizer)
					f.write('_' * 70)
					f.write('\nINFO about generation {}:\n'.format(i + 1))
					for chromosome in self.chromosomes:
						f.write('chromosome {} gives value: {}\n'.format(chromosome, self.function(*chromosome)))
					f.write('max value for this generation: {}\n'.format(self.calculate(optimizer)))
			else:
				raise ValueError(optimizer + 'should be max or min')

		self.plotGA(chromosomes_number, generations_number, optimizer)


