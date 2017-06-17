import numpy as np
import itertools

MAX_DISTANCE = 250

def distanceMatrix():
    return np.matrix([
    [0,  10, 20, 5,  18],
    [10, 0,  15, 32, 10],
    [20, 15, 0,  25, 16],
    [5,  32, 25, 0,  35],
    [18, 10, 16, 35, 0],
    ])

def path(state):
    path = []
    for colIdx in range(state.shape[1]):
        path.append(np.argmax(state[:,colIdx]))
    return path


def pathDistance(distanceMatrix, path):
    distance = 0
    for index in range(len(path))[1:]:
        distance += distanceMatrix[path[index - 1], path[index]]
    return distance


def isPathValid(state):
    # count the number of times a city was visited, each city should be
    duplicateVisits = 0
    dupRowIdx = None
    for rowIdx in range(state.shape[0]):
        timesVisited = np.sum(state[rowIdx, :])

        # visiting a city 1 or 2 times are the only numbers which are valid
        if timesVisited != 1 and timesVisited != 2:
            return False

        # it is permissible (and expected) to visit the starting city twice
        if timesVisited == 2:
            duplicateVisits += 1
            dupRowIdx = rowIdx

    # ensure that there is only one duplicate visit
    if duplicateVisits != 1:
        return False

    # ensure that it is exactly the first and last node that are duplicates
    if state[dupRowIdx,0] != 1 or state[dupRowIdx,-1] != 1:
        return False

    # it is never valid to visit muliple cities simultaneously
    for colIdx in range(state.shape[1]):
        citiesVisitedAtOnce = np.sum(state[:, colIdx])
        if citiesVisitedAtOnce != 1:
            return False

    return True
