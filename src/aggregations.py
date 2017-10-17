import os
from pprint import pprint
from matplotlib import pyplot
from numpy import array, transpose, mean, std

from data import dataSmall, dataBig
from randomSolution import randomChromosomeFromData, generateRandomSolution
from geneticAlg import generatePopulation

# Configure here, use smaller numbers if you want it to run faster
ITERATIONS = 100
MAX_GENERATIONS = 100
MAX_POPULATION = 500

def generateAlgSolution(maxGenerations = 50, maxPopulation = MAX_POPULATION, data = {}):
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

def generateRandSolution(maxGenerations = 50, maxPopulation = MAX_POPULATION, data = {}):
	isBigDataset = len(data) > 300

	return generateRandomSolution(
		maxGenerations = maxGenerations,
		testsInChromosome = 20 if isBigDataset else 5,
		data = data,
		dataName = 'Big Dataset' if isBigDataset else 'Small Dataset'
	)


results = {
	'smallAlgSolutions': [],
	'bigAlgSolutions': [],
	'smallRandSolutions': [],
	'bigRandSolutions': []
}


print('Running algorithms on all datasets')
print()
# How many times to run algorithms
for i in range(ITERATIONS):
	print('Iteration {}'.format(i))
	results['smallAlgSolutions'].append(generateAlgSolution(data = dataSmall, maxGenerations = MAX_GENERATIONS))
	results['bigAlgSolutions'].append(generateAlgSolution(data = dataBig, maxGenerations = MAX_GENERATIONS))
	results['smallRandSolutions'].append(generateRandomSolution(data = dataSmall, maxGenerations = MAX_GENERATIONS))
	results['bigRandSolutions'].append(generateRandSolution(data = dataBig, maxGenerations = MAX_GENERATIONS))


plotsPath = os.path.dirname(os.path.realpath(__file__)) + '/../aggregatePlots/'
aggregateStats = []

print('Aggregating Stats for Each Iteration')
print('Plots saved in aggregatePlots folder in repository root.')
print('\n Ctrl + C to close all figures.')

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
	pyplot.suptitle('Aggregate Fitness in {} \n for {} Iterations'.format(result, ITERATIONS))
	pyplot.xlabel('Generation')
	pyplot.ylabel('Fitness')

	for aggregate in aggregateStats:
		pyplot.plot(aggregateStats[aggregate], label = aggregate)

	pyplot.legend(loc='upper right')
	pyplot.savefig(plotsPath + 'AggregateFitness{}'.format(result) + '.png')
pyplot.show()

print('\n Done! \n ')
