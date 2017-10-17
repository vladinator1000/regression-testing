# https://imgur.com/a/pLTxz
# Average Percentage of Faults Detected (Pandey and Shrivastava, 2011) 
def APFD(tests = [[]]):
	numberOfTests = len(tests)
	numberOfFaults = len(tests[0])
	sumOfTestPositions = 0.0

	currentFaultsFound = [0 for i in range(numberOfFaults)]

	# For every test case, iterate over every fault and check if it has been found 
	for testIndex, testCase in enumerate(tests):
		for faultIndex, fault in enumerate(testCase):
			if fault == 1 and currentFaultsFound[faultIndex] == 0:
				sumOfTestPositions += testIndex + 1
				currentFaultsFound[faultIndex] = 1

	# For every fault that wasn't found, add numberOfTests + 0.5 to the sum
	# https://i.imgur.com/u262XEv.jpg <-- here's why (because Steve Gardiner is smart)
	for i in range(currentFaultsFound.count(0)):
		sumOfTestPositions += numberOfTests + 0.5

	return 1.0 - (sumOfTestPositions / (numberOfTests * numberOfFaults)) + (1.0 / (2.0 * numberOfTests))