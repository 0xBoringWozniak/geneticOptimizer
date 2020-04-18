import numpy 				as np
import numpy.random 		as rd
import pandas 				as pd
import matplotlib.pyplot 	as plt
import matplotlib.animation as animation
import tkinter.scrolledtext as tkst
import tkinter 				as tk


from tkinter 				import *
from accessify 				import protected
from matplotlib 			import cm
from mpl_toolkits.mplot3d 	import Axes3D
from matplotlib.ticker 		import LinearLocator, FormatStrFormatter
from collections 			import OrderedDict

import sys, os

from func import Func


class OptimizerGA:
	def __init__(self, function):
		self.function = function

	@protected
	def generate_new_part(self, chromosomes, mutation=False, mutation_range=2, optimizer='min'):
		values = [self.function(*chromosome) for chromosome in chromosomes]
		chromosomesDict = dict(zip([str(i) for i in range(4)], values))

		if optimizer == 'min':
			chromosomesDict = OrderedDict(sorted(chromosomesDict.items(), key=lambda t: t[1]))
		elif optimizer == 'max':
			chromosomesDict = OrderedDict(sorted(chromosomesDict.items(), key=lambda t: -t[1]))
		else:
			raise ValueError(str(optimizer) + ' should be max or min')

		chromosome_indexes = list()

		for chromosome_index in chromosomesDict.keys():
			chromosome_indexes.append(chromosome_index)

		good_chromosome = chromosomes[int(chromosome_indexes[2])]
		better_chromosome = chromosomes[int(chromosome_indexes[1])]
		best_chromosome = chromosomes[int(chromosome_indexes[0])]

		new_part = np.array([	[better_chromosome[0] + float(mutation_range * mutation * rd.rand(1) - (mutation_range / 2)), best_chromosome[1]],
								[good_chromosome[0]   + float(mutation_range * mutation * rd.rand(1) - (mutation_range / 2)), best_chromosome[1]],
								[best_chromosome[0], better_chromosome[0] + float(mutation_range * mutation * rd.rand(1) - (mutation_range / 2))],
								[best_chromosome[0], good_chromosome[1]   + float(mutation_range * mutation * rd.rand(1) - (mutation_range / 2))]])
		return new_part

	@protected
	def next_generation(self, mutation=False, mutation_range=2, optimizer='min'):
		part = np.array([self.chromosomes[j] for j in range(0 , 4)])
		new_population = self.generate_new_part(part, mutation, mutation_range, optimizer)

		for parts_number in range(1, int(len(self.chromosomes) / 4)):
			part = np.array([self.chromosomes[j] for j in range(parts_number * 4, (parts_number + 1) * 4)])
			new_part = self.generate_new_part(part, mutation, mutation_range, optimizer)
			new_population = np.append(new_population, new_part, axis=0)

		return new_population

	@protected
	def calculate(self, optimizer='min'):
		if optimizer == 'min':
			return min([self.function(*chromosome) for chromosome in self.chromosomes])
		elif optimizer == 'max':
			return max([self.function(*chromosome) for chromosome in self.chromosomes])
		else:
			raise ValueError(optimizer + ' should be max or min')

	@protected
	def plotGA(self, chromosomes_number, generations_number, optimizer, save=False):
		data = pd.concat([pd.read_csv('generations/generation_{}.csv'.format(i + 1), index_col=0) 
								for i in range(generations_number)], ignore_index=True)

		data['time'] = [i for i in range(chromosomes_number * generations_number)]

		def update_graph(num):
			df = data[abs(num * chromosomes_number - data['time']) <= 2 * chromosomes_number]
			graph.set_data(np.array(df['x']), np.array(df['y']))
			graph.set_3d_properties(np.array(df['f(x, y)']))
			title.set_text('generation={}'.format(num + 1))
			return title, graph, 

		fig = plt.figure(figsize = (15, 8), num='GA animation')

		ax = fig.add_subplot(111, projection='3d')


		# Make data.
		X = np.arange(-4, 4, 0.25)
		Y = np.arange(-4, 4, 0.25)
		X, Y = np.meshgrid(X, Y)
		Z = self.function(X, Y)


		# set colormap if it is needed
		theCM = cm.get_cmap()
		theCM._init()
		alphas = np.abs(np.linspace(-1, 1, int(theCM.N)))
		theCM._lut[:-3,-1] = alphas

		# Plot the surface.
		surf = ax.plot_surface(X, Y, Z, cmap=theCM,
								linewidth=0, antialiased=True, alpha=0.6)

		title = ax.set_title('GA-optimizer plot')



		df = data[data['time'] == 0]
		graph, = ax.plot(np.array(df['x']), np.array(df['y']), np.array(df['f(x, y)']), 
								linestyle="", c='black', marker='2', ms=2)


		anim = animation.FuncAnimation(fig, update_graph, generations_number, interval=200, save_count=True)

		# Customize the z axis.
		ax.set_zlim(-5, 5)
		ax.zaxis.set_major_locator(LinearLocator(10))
		ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

		ax.set_xlabel('X')
		ax.set_ylabel('Y')
		ax.set_zlabel('Z')

		# Add a color bar which maps values to colors.
		fig.colorbar(surf, shrink=0.8, aspect=3)

		plt.show()
		if save:
			anim.save('results/GA-animation.gif', writer='imagemagick', fps=60)
	
	def startGA(self, chromosomes_number=4, generations_number=10, 
				mutation=False, mutation_range=2, optimizer='min', 
				statistics=True, save=False, plot=True):
		self.chromosomes = np.array([(mutation_range * rd.rand(2) - int(mutation_range / 2)) for i in range(chromosomes_number)])

		f = open('results/GA-statistics.txt', 'w')
		for i in range(generations_number):
			self.chromosomes = self.next_generation(mutation, float(mutation_range / (i + 1)), optimizer)
			df = pd.DataFrame(self.chromosomes, columns=['x', 'y'])
			x = np.array(df['x'])
			y = np.array(df['y'])
			df['f(x, y)'] = self.function(x, y)
			df.to_csv("generations/generation_{}.csv".format(i + 1))
			
			
			f.write('_' * 70)
			f.write('\nINFO about generation {}:\n'.format(i + 1))
			for chromosome in self.chromosomes:
				f.write('chromosome {} gives value: {}\n'.format(chromosome, self.function(*chromosome)))
			f.write('{} value for this generation: {}\n'.format(optimizer, self.calculate(optimizer)))

		f.close()
		
		if plot:
			self.plotGA(chromosomes_number, generations_number, optimizer, save)

		if not(save):
			for i in range(generations_number):
				os.remove("generations/generation_{}.csv".format(i + 1))

