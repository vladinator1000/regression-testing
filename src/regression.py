import os
from re import sub
from numpy import trapz, array
from pprint import pprint

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)

txtFile = os.path.join(__location__, 'data-small.txt')

data = {}
currentKey = ''
for line in open(txtFile, 'r'):
    text = line.strip().replace(':', '')

    if 'unit' in text:
        currentKey = text
        data[currentKey] = []

    elif 'v' not in text:
        data[currentKey].append(int(text))


pprint(data)
sort = sorted(data, key = lambda key: int(sub('[^0-9]','', key)))
# pprint(sort)


# y = [5, 20, 4, 18, 19, 18, 7, 4]
#
# # Compute the area using the composite trapezoidal rule.
# # https://en.wikipedia.org/wiki/Trapezoidal_rule
#
# for i in range(5):
#     print(trapz(y))
