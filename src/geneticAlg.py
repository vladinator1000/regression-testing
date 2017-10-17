import random
from sys import setrecursionlimit
from pprint import pprint
from copy import deepcopy
from itertools import chain
from numpy import mean, std

from APFD import APFD

setrecursionlimit(1500)

def tournament(generation = [], probabilityFitterWins = 0.8):
	first = random.choice(generation)
	second = random.choice(generation)

	if random.random() < probabilityFitterWins:
		# Fitness at index 2, bigger is better
		if first[2] > second[2]:
			return first
		else:
			return second

	else:
		if first[2] < second[2]:
			return first
		else:
			return second


def mutateGeneration(generation = [], probability = 0.15, data = {}):
	newGeneration = []

	for chromosome in generation:
		if random.random() < probability:
			# Copy, not reference
			newChromosome = deepcopy(chromosome)

			# Replace a test inside a chromosome with a random one
			randomIndex = random.randrange(len(chromosome[1]))
			newTestName = random.choice(list(data))

			newChromosome[0][randomIndex] = newTestName
			newChromosome[1][randomIndex] = data[newTestName]

			newGeneration.append(newChromosome)
		else:
			newGeneration.append(chromosome)

	return newGeneration

def crossover(parent1, parent2, noCrossRate = 0.10, fitnessFunction = APFD, data = {}):
	if random.random() < noCrossRate:
		return (parent1, parent2)

	parentLength = len(parent1[0])
	randomIndex = random.randrange(parentLength)

	newNames1 = list(chain(parent1[0][:randomIndex], parent2[0][randomIndex:]))
	newNames2 = list(chain(parent2[0][:randomIndex], parent1[0][randomIndex:]))


	def removeDuplicates(values):
		output = []
		seen = set()
		for value in values:
			# If value has not been encountered yet,
			# add it to both list and set.
			if (value) not in seen:
				output.append(value)
				seen.add(value)
		return output

	newNames1 = removeDuplicates(newNames1)
	newNames1 = removeDuplicates(newNames1)

	# Fill in arrays until long as parents
	while len(newNames1) != parentLength:
		lengthDifference = parentLength - len(newNames1)

		for item in random.sample(list(data), lengthDifference):
			newNames1.append(item)

		newNames1 = removeDuplicates(newNames1)

	while len(newNames2) != parentLength:
		lengthDifference = parentLength - len(newNames2)

		for item in random.sample(list(data), lengthDifference):
			newNames2.append(item)

		newNames2 = removeDuplicates(newNames2)

	newTests1 = []
	newTests2 = []

	for itemA, itemB in zip(newNames1, newNames2):
		newTests1.append(data[itemA])
		newTests2.append(data[itemB])

	# Tuple of tuples
	return (
		(newNames1, newTests1, APFD(newTests1)),
		(newNames2, newTests2, APFD(newTests2)),
	)

def generatePopulation(
	old = [],
	currentGeneration = 0,
	maxGenerations = 500,
	selectionFunction = tournament,
	mutationRate = 0.04,
	noCrossRate = 0.15,
	data = {},
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
	fitnessesForGen = list(map(lambda item: item[2], old))
	newFittest = max(old, key = lambda item: item[2])

	# Fitness deltas between fittest specimen
	fitnessDifference = newFittest[2] - fittest[2]

	# print('\n')
	# print('{}...'.format(newFittest[0][0: 7]))
	# print('Generation {}, fittest: {}, delta: {}'.format(currentGeneration, newFittest[2], fitnessDifference))

	new = []

	if currentGeneration < maxGenerations:
		while len(new) < len(old):
			# Crossover returns tuple of two
			children = crossover(
				selectionFunction(old),
				selectionFunction(old),
				noCrossRate = noCrossRate,
				data = data
			)

			for child in children:
				new.append(child)

		return generatePopulation(
			mutateGeneration(new, probability = mutationRate, data = data),
			currentGeneration + 1,
			maxGenerations,
			mutationRate = mutationRate,
			noCrossRate = noCrossRate,
			data = data,
			fittest = newFittest,
			fitnessDeltas = fitnessDeltas + [fitnessDifference],
			fittestForEachGen = fittestForEachGen + [newFittest[2]],
			dataName = dataName,
			fitnessStats = {
				'min': fitnessStats['min'] + [min(fitnessesForGen)],
				'max': fitnessStats['max'] + [max(fitnessesForGen)],
				'mean': fitnessStats['mean'] + [mean(fitnessesForGen)],
				'std': fitnessStats['std'] + [std(fitnessesForGen)]
			}
		)

	return {
		'generation': currentGeneration,
		'fittest': fittest,
		'fittestForEachGen': fittestForEachGen,
		'deltas': fitnessDeltas,
		'dataName': dataName,
		'name': 'Genetic Alg',
		'fitnessStats': fitnessStats
	}
