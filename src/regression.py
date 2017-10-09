import os
import random
from re import sub
from pprint import pprint
from matplotlib import pyplot

#  Parse data
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


sampleKeys = random.sample(list(data), 5)

# sums = map(lambda key: sum(data[key]), sampleKeys)
# pprint(sums)

for key in sampleKeys:
	print()

# Each solution has 5 tests
# Get APFD for each test (https://imgur.com/a/pLTxz)
