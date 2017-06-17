import utils
import numpy as np
import itertools

def shortestPaths(distanceMatrix):
    shortestPathDistance = None
    shortestPaths = [] # track all valid paths with best distance

    paths = itertools.permutations(range(distanceMatrix.shape[0]))

    for curPath in paths:
        # revisit the first node at the end of the route
        curPath = list(curPath) + [curPath[0]]

        pathDistance = utils.pathDistance(distanceMatrix, curPath)

        if shortestPathDistance == None or pathDistance < shortestPathDistance:
            shortestPathDistance = pathDistance

            # we found a better candidate, delete all solutions tracked
            shortestPaths = []

        if pathDistance == shortestPathDistance:
            shortestPaths.append(curPath)

    return shortestPaths

def longestPath(distanceMatrix):
    longestPath = None
    longestPathDistance = None

    paths = itertools.permutations(range(distanceMatrix.shape[0]))

    for curPath in paths:
        # revisit the first node at the end of the route
        curPath = list(curPath) + [curPath[0]]

        pathDistance = utils.pathDistance(distanceMatrix, curPath)

        if longestPathDistance == None or pathDistance > longestPathDistance:
            longestPath = curPath
            longestPathDistance = pathDistance

    return [longestPath]
