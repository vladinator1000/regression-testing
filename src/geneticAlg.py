import os, sys
import random
import csv
from pprint import pprint
from copy import deepcopy
from itertools import chain

sys.setrecursionlimit(1500)

# Parse .txt files
__location__ = os.path.realpath(
	os.path.join(os.getcwd(), os.path.dirname(__file__))
)

smallTxtFile = os.path.join(__location__, 'data-small.txt')
bigTxtFile = os.path.join(__location__, 'data-big.txt')


dataSmall = {}
currentKey = ''
for line in open(smallTxtFile, 'r'):
	text = line.strip().replace(':', '')

	if 'unit' in text:
		#  Format text a bit
		currentKey = text.replace('unitest', 'test')
		dataSmall[currentKey] = []

	elif 'v' not in text:
		dataSmall[currentKey].append(int(text))

with open(bigTxtFile, mode='r') as inFile:
	reader = csv.reader(inFile)
	dataBig = {rows[0]:list(map(int, rows[1:])) for rows in reader}


# https://imgur.com/a/pLTxz
# Average Percentage of Faults Detected (Pandey and Shrivastava, 2011):
def APFD(tests = [[]]):
	numberOfTests = len(tests)
	numberOfFaults = len(tests[0])
	sumOfTestPositions = 0.0

	# Keep track of current faults found
	faultsFoundBuffer = [0 for i in range(numberOfFaults)]

	for testIndex, testCase in enumerate(tests):
		for faultIndex, fault in enumerate(testCase):
			if fault == 1 and faultsFoundBuffer[faultIndex] == 0:
				sumOfTestPositions += testIndex + 1
				faultsFoundBuffer[faultIndex] = 1

	# For every fault that wasn't found, add numberOfTests + 0.5 to the sum
	# https://i.imgur.com/u262XEv.jpg <-- here's why
	for i in range(faultsFoundBuffer.count(0)):
		sumOfTestPositions += numberOfTests + 0.5

	return 1.0 - (sumOfTestPositions / (numberOfTests * numberOfFaults)) + (1.0 / (2.0 * numberOfTests))

# This will make up our population
def randomTestsFromData(howMany = 5, data = {}):
	names = []
	tests = []

	for testName in random.sample(list(data), howMany):
		names.append(testName)
		tests.append(data[testName])

	return (names, tests, APFD(tests))

def tournament(generation = []):
	first = random.choice(generation)
	second = random.choice(generation)

	# Fitness at index 2, bigger is better
	if first[2] > second[2]:
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
	mutationRate = 0.05,
	noCrossRate = 0.05,
	data = {}
):
	fittest = max(old, key = lambda item: item[2])

	print('\n')
	print(fittest[0])
	# First 4 rows of test cases
	for i in range(4):
		print(fittest[1][i])
	print('...')
	print('Generation {}, fittest: {}'.format(currentGeneration, fittest[2]))

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
			selectionFunction = selectionFunction,
			data = data
		)

	return {
		'currentGeneration': currentGeneration,
		'selection': selectionFunction.__name__,
		'population': old
	}



# Generate initial population :
# List of tuples in the form of ((testName1, ...), (test1, ...), fitness)
population = []

for i in range(1000):
	population.append(randomTestsFromData(howMany = 20, data = dataBig))

result = generatePopulation(population, maxGenerations = 1000, data = dataBig)
