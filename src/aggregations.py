from pprint import pprint
from matplotlib import pyplot
from numpy import array, transpose, mean, std

from data import dataSmall, dataBig
from randomSolution import randomChromosomeFromData, generateRandomSolution
from geneticAlg import generatePopulation

# test = array([
# 	[11, 12, 13],
# 	[21, 22, 23],
# 	[31, 32, 33],
# 	[41, 420, 4300]
# ])
# print(transpose(test))
#

def generateAlgSolution(maxGenerations = 50, maxPopulation = 50, data = {}):
	population = []

	isBigDataset = len(data) > 300

	for i in range(maxPopulation):
		population.append(
			randomChromosomeFromData(
				testsInChromosome = 20 if isBigDataset else 5,
				data = data,
			)
		)

	return generatePopulation(
		population,
		maxGenerations = maxGenerations,
		data = data,
		dataName = 'Big Dataset' if isBigDataset else 'Small Dataset'
	)

def generateRandSolution(maxGenerations = 50, maxPopulation = 50, data = {}):
	isBigDataset = len(data) > 300

	return generateRandomSolution(
		maxGenerations = maxGenerations,
		testsInChromosome = 20 if isBigDataset else 5,
		data = data,
		dataName = 'Big Dataset' if isBigDataset else 'Small Dataset'
	)



smallAlgSolutions = []
bigAlgSolutions = []
smallRandSolutions = []
bigRandSolutions = []

results = {
	'smallAlgSolutions': [],
	'bigAlgSolutions': [],
	'smallRandSolutions': [],
	'bigRandSolutions': []
}

for i in range(100):
	results['smallAlgSolutions'].append(generateAlgSolution(data = dataSmall))
	results['bigAlgSolutions'].append(generateAlgSolution(data = dataBig))
	results['smallRandSolutions'].append(generateAlgSolution(data = dataSmall))
	results['bigRandSolutions'].append(generateAlgSolution(data = dataBig))



aggregateStats = []

for i, result in enumerate(results):
	stats = {
		'min': [],
		'max': [],
		'mean': [],
		'std': []
	}

	for solution in results[result]:
		for stat in solution['fitnessStats']:
			stats[stat].append(solution['fitnessStats'][stat])

	aggregateStats = {
		'min': [],
		'max': [],
		'mean': [],
		'std': []
	}

	for stat in stats:
		for column in transpose(stats[stat]):
			aggregateStats[stat].append(mean(column))




	pyplot.figure(i)
	pyplot.suptitle('Aggregate Fitness in {}'.format(result))
	pyplot.xlabel('Generation')
	pyplot.ylabel('Fitness')

	for aggregate in aggregateStats:
		pyplot.plot(aggregateStats[aggregate], label = aggregate)

	pyplot.legend(loc='upper right')

pyplot.show()

# for solution in solutions:
# 	for stat in solution['fitnessStats']:
# 		stats[stat].append(solution['fitnessStats'][stat])
	# print('\n')


# pprint(stats['min'][:3])
