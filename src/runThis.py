from matplotlib import pyplot

from data import dataSmall, dataBig
from randomSolution import randomChromosomeFromData, generateRandomSolution
from geneticAlg import generatePopulation


# Generate initial populations:
# List of tuples in the form of ((testName1, ...), (test1, ...), fitness)
smallPopulation = []
bigPopulation = []

for i in range(500):
	smallPopulation.append(randomChromosomeFromData(howMany = 5, data = dataSmall))
	bigPopulation.append(randomChromosomeFromData(howMany = 20, data = dataBig))


solutions = [
	generatePopulation(smallPopulation, maxGenerations = 50, data = dataSmall, name = 'Small Dataset'),
	generatePopulation(bigPopulation, maxGenerations = 50, data = dataBig, name = 'Big Dataset'),
]


for i, solution in enumerate(solutions):
	pyplot.figure(i)
	pyplot.suptitle('Improvement Rate in {}'.format(solution['name']))
	pyplot.xlabel('Generation')
	pyplot.ylabel('Fitness Improvement')
	pyplot.plot(solution['deltas'])

pyplot.show()
