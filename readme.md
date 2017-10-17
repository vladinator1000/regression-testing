# Assignment 2
This repo can be found at: https://github.com/savovs/regression-testing

It aims to order tests from a pre-defined dataset in an optimal order, maximising
the Average Percentage of Faults Detected by each batch of tests.

Two algorithms are compared, a Genetic Algorithm and a Random approach.

The GA iterates through generations, using tournament selection, mutation
and crossover (making sure all tests in chromosome are unique). All of these
operations have an associated probability parameter.

The Random method creates random permutations of a fixed length, taking tests
from the dataset. The fitness outputs of both random and GA are observed in the
plots folder.

To quickly check it out, run `/src/runThis.py`, it will show stats for one generation only.
To re-run the statistics, run `/src/aggregations.py`

![GA](/aggregatePlots/AggregateFitnessbigAlgSolutions.png) ![Random](/aggregatePlots/AggregateFitnessbigRandSolutions.png)

In the big dataset, bigAlg (which is the GA) has more reliable values than random
generation, because the standard deviation is lower. In the GA the deviation
is falling, where in the random method, the deviation is rising. While both
mean values for rand and GA are rising with generations, the GA experiences
a much steeper rise than the random method (which platoes and doesn't rise as high).
A distance of roughly 0.2 fitness can be observed between the mean values of
the algorithms. The disadvantage of the GA is that it starts off with low fitness,
while Random has a chance to get lucky and find a high value.
