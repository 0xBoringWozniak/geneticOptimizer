# MaxMinFuncByGeneticAlgorithm


** python3 main.py to run this programme and open GUI **


This programme approximately calculates a minimum or a maximum of function with two parameters based on genetic algorithm.
Each individual is one chromosome (x, y) and because of it an individual and a chromosome have the same meaning, a generation consists of parts where one part is 4 individuals, as consequence, number of chromosomes is multiple of 4.

A genetic algorithm makes crossovering in each part separately after what appends it to a generation. A crossover principle is:

(x_better, y_best), (y_better, y_best), (x_best, y_better), (x_best, y_good)

where (x_best, y_best), (x_better, y_better), (x_good, y_good) are selected individs.

A mutation can be chosen randomly in any gens (it can be configured in method startGA_with_statistics).
A zero-generation fill with random float numbers in [-chromosomes_number / 2, chromosomes_number).
Results are shown in the screen and also are saved in 'GA-statistics.txt'.



 
