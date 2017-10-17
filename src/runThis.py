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
	smallPopulation.append(randomChromosomeFromData(howMany = 5, data = dataSmall))
	bigPopulation.append(randomChromosomeFromData(howMany = 20, data = dataBig))



solutions = []
for i in range(2):
	solutions.append((
		generatePopulation(smallPopulation, maxGenerations = 50, data = dataSmall, dataName = 'Small Dataset'),
		generatePopulation(bigPopulation, maxGenerations = 50, data = dataBig, dataName = 'Big Dataset'),
		generateRandomSolution(maxGenerations = 50, data = dataSmall, dataName = 'Small Dataset'),
		generateRandomSolution(maxGenerations = 50, data = dataBig, dataName = 'Big Dataset')
	))

stats = {}

for solution in solutions:
	for case in solution:
		for stat in case['fitnessStats']:
			stats[stat] = case['fitnessStats'][stat]
			print(stats[stat])
			# print(case['fitnessStats'].keys())
			print('\n')

print()

# pprint(solutions[0][]['fitnessStats'])

# for i, solution in enumerate(solutions):
# 	pyplot.figure(i)
# 	pyplot.suptitle('Fitness in {}, using {}'.format(solution['dataName'], solution['name']))
# 	pyplot.xlabel('Generation')
# 	pyplot.ylabel('Fitness')
#
# 	for stat in solution['fitnessStats']:
# 		pyplot.plot(solution['fitnessStats'][stat], label = stat)
#
# 	pyplot.legend(loc='upper right')
#
# pyplot.show()
