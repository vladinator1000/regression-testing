from pprint import pprint
from matplotlib import pyplot

from data import dataSmall, dataBig
from randomSolution import randomChromosomeFromData, generateRandomSolution
from geneticAlg import generatePopulation


# Generate initial populations:
# List of tuples in the form of ((testName1, ...), (test1, ...), fitness)
smallPopulation = []
bigPopulation = []

for i in range(500):
	smallPopulation.append(randomChromosomeFromData(testsInChromosome = 5, data = dataSmall))
	bigPopulation.append(randomChromosomeFromData(testsInChromosome = 20, data = dataBig))



solutions = [
	generatePopulation(smallPopulation, maxGenerations = 50, data = dataSmall, dataName = 'Small Dataset'),
	generatePopulation(bigPopulation, maxGenerations = 50, data = dataBig, dataName = 'Big Dataset'),
	generateRandomSolution(maxGenerations = 50, data = dataSmall, dataName = 'Small Dataset'),
	generateRandomSolution(maxGenerations = 50, data = dataBig, dataName = 'Big Dataset')
]


for i, solution in enumerate(solutions):
	pyplot.figure(i)
	pyplot.suptitle('Fitness in {}, using {}'.format(solution['dataName'], solution['name']))
	pyplot.xlabel('Generation')
	pyplot.ylabel('Fitness')

	for stat in solution['fitnessStats']:
		pyplot.plot(solution['fitnessStats'][stat], label = stat)

	pyplot.legend(loc='upper right')

pyplot.show()

# This shows stats from only one iteration.
# Check out aggregations.py if you want to run statistical aggregations
# of multiple iterations of the algorithms.
