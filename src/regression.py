import os
import random
from pprint import pprint
# from matplotlib import pyplot

# Parse .txt file
__location__ = os.path.realpath(
	os.path.join(os.getcwd(), os.path.dirname(__file__))
)

txtFile = os.path.join(__location__, 'data-small.txt')

data = {}
currentKey = ''
for line in open(txtFile, 'r'):
	text = line.strip().replace(':', '')

	if 'unit' in text:
		#  Format text a bit
		currentKey = text.replace('unitest', 'test')
		data[currentKey] = []

	elif 'v' not in text:
		data[currentKey].append(int(text))


# https://imgur.com/a/pLTxz 
# Average Percentage of Faults Detected (Pandey and Shrivastava, 2011):
def APFD(tests = [[]]):
	numberOfTests = len(tests)
	numberOfFaults = len(tests[0])
	sumOfFaultIndexes = 0

	# Initial list of zeros
	faultsFound = [0 for i in range(numberOfFaults)]
	

	for faults in tests:
		for index, fault in enumerate(faults):
			if fault == 1 and faultsFound[index] == 0:
				# Add to index sum (counting from 1) 
				sumOfFaultIndexes += index + 1
				faultsFound[index] = 1
			else:
				sumOfFaultIndexes += numberOfFaults + 0.5

	return 1 - (sumOfFaultIndexes / (numberOfTests * numberOfFaults)) + (1 / (2 * numberOfTests))

# This will make up our population 
def randomTestsFromData(howMany = 5):
	names = []
	tests = []

	for testName in random.sample(list(data), howMany):
		names.append(testName)
		tests.append(data[testName])

	return (names, tests, APFD(tests))

# Generate population :
# List of tuples in the form of ((testName1, ...), (test1, ...), fitness)
# firstGeneration = []

# for i in range(1):
# 	firstGeneration.append(randomTestsFromData())


def tournament(generation = []):
	first = random.choice(generation)
	second = random.choice(generation)

	# Fitness at index 3, bigger is better
	if first[3] > second[3]:
		return first
	else:
		return second

def mutateGeneration(generation = [], probability = 0.15):
	newGeneration = []

	for chromosome in generation:
		if random.random() < probability:
			newChromosome = chromosome

			# Replace a test inside a chromosome with a random one 
			randomIndex = random.randrange(len(chromosome[1]))
			newTestName = random.choice(list(data))

			newChromosome[0][randomIndex] = newTestName
			newChromosome[1][randomIndex] = data[newTestName]

			newGeneration.append(newChromosome)
			
			print(newChromosome, )
		else:
			newGeneration.append(chromosome)

# mutateGeneration(firstGeneration, 1)

test = [[0, 0, 0, 0, 0, 0, 1, 0, 0] for i in range(5)]

# print(test)
print(APFD(test))