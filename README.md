# function optimizer based on genetic algorithms


### How to install

install package geneticOptimizer in env - it can be done, for instance, with the help of github actions, PyCharm 
or manually from github repo.

be sure that in geneticOptimizer/ you have folders generations and results


### How to use

**env/bin/python3 -m geneticOptimizer** to run this programme and open settings-GUI with several fields:
- f(x, y) input string
- chromosomes=individs input string
- generations number input string
- optimizer function (min or max)

Furthermore, optional fields:

- mutation - add a mutation to each part(4 individuals) of a new generation
- show statistics - show accurate information about each generation
- save all files - save in geneticOptimizer/result statistics with animation in .gif and GA-Statistics.csv
                   and  in geneticOptimizer/generations .csv data with cols x, y, f(x, y)
- show plot - show an animation of an evalution



### About an algorithm 
This programme approximately calculates a minimum or a maximum of function with two parameters based on genetic algorithm.
Each individual is one chromosome (x, y) and because of it an individual and a chromosome have the same meaning, a generation consists of parts where one part is 4 individuals, as consequence, a number of chromosomes is multiple of 4.

A genetic algorithm makes crossovering in each part separately after what appends it to a generation. A crossover principle is:

(x_better, y_best), (y_better, y_best), (x_best, y_better), (x_best, y_good)

where (x_best, y_best), (x_better, y_better), (x_good, y_good) are selected individs.
A mutation can be chosen randomly in any gens (it can be configured in method startGA_with_statistics).
A zero-generation fill with random float numbers in [-chromosomes_number / 2, chromosomes_number).


# It is planned:

- [] Add mutation options such as a percentage of mutations genes, a step of mutation, a kind of mutation
- [] Add selection options based on different GA
- [] Add more metrics for GA and more info in statistics, for instance, a time, a fitness etc.
- [] Add a custom list of functions which can illustrate how the package works



 
