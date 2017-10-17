import os
import csv

# Parse .txt files into dictionaries in the form { 'test1': [0, 1, ...], ...}
__location__ = os.path.realpath(
	os.path.join(os.getcwd(), os.path.dirname(__file__))
)

smallTxtFile = os.path.join(__location__, '../data-small.txt')
bigTxtFile = os.path.join(__location__, '../data-big.txt')

# Import this
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

	# Import this
	dataBig = { rows[0]:list(map(int, rows[1:])) for rows in reader }
