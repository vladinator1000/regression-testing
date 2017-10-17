import random

from APFD import APFD


def randomChromosomeFromData(howMany = 5, data = {}):
	names = []
	tests = []

	for testName in random.sample(list(data), howMany):
		names.append(testName)
		tests.append(data[testName])

	return (names, tests, APFD(tests))

def generateRandomSolution():
	return {}