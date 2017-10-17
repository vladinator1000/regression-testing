import random
from numpy import mean, std

from APFD import APFD


def randomChromosomeFromData(howMany = 5, data = {}):
	names = []
	tests = []

	for testName in random.sample(list(data), howMany):
		names.append(testName)
		tests.append(data[testName])

	return (names, tests, APFD(tests))

# Each generation has 1 specimen
def generateRandomSolution(
	maxGenerations = 100,
	data = {},
	currentGeneration = 0,
	fittest = ((), (), 0.0),
	fitnessDeltas = [],
	fittestForEachGen = [],
	dataName = '',
	fitnessStats = {
		'min': [],
		'max': [],
		'mean': [],
		'std': []
	},
):
	newChromosome = randomChromosomeFromData(5, data = data)

	if newChromosome[2] > fittest[2]:
		newFittest = newChromosome
		fitnessDifference = newChromosome[2] - fittest[2]
	else:
		newFittest = fittest
		fitnessDifference = 0.0

	fittestForEachGen += [newFittest[2]]

	if currentGeneration < maxGenerations:
		return generateRandomSolution(
			maxGenerations = maxGenerations,
			data = data,
			currentGeneration = currentGeneration + 1,
			fittest = newFittest,
			fitnessDeltas = fitnessDeltas + [fitnessDifference],
			fittestForEachGen = fittestForEachGen + [newFittest[2]],
			dataName = dataName,
			fitnessStats = {
				'min': fitnessStats['min'] + [min(fittestForEachGen)],
				'max': fitnessStats['max'] + [max(fittestForEachGen)],
				'mean': fitnessStats['mean'] + [mean(fittestForEachGen)],
				'std': fitnessStats['std'] + [std(fittestForEachGen)]
			}
		)

	return {
		'generation': currentGeneration,
		'fittest': fittest,
		'fittestForEachGen': fittestForEachGen,
		'deltas': fitnessDeltas,
		'dataName': dataName,
		'name': 'Random Generation',
		'fitnessStats': {
			'min': fitnessStats['min'] + [min(fittestForEachGen)],
			'max': fitnessStats['max'] + [max(fittestForEachGen)],
			'mean': fitnessStats['mean'] + [mean(fittestForEachGen)],
			'std': fitnessStats['std'] + [std(fittestForEachGen)]
		}
	}
