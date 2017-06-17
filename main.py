import utils
import boltzmann
import bruteforce
import sys

class bcolors:
  HEADER = '\033[95m'
  BLUE = '\033[94m'
  GREEN = '\033[92m'
  YELLOW = '\033[93m'
  RED = '\033[91m'
  NORMAL = '\033[0m'
  BOLD = '\033[1m'

def show(title, paths, dist):
    print "%s%s paths%s (Distance=%d):" % (bcolors.HEADER, title.title(), bcolors.NORMAL, dist)
    for path in sorted(paths):
        print "   ", path
    print

if __name__ == "__main__":
    distanceMatrix = utils.distanceMatrix()

    print "%sDistance Matrix%s" % (bcolors.HEADER, bcolors.NORMAL)
    print "  ",str(distanceMatrix).replace("\n","\n   ")
    print

    comparisons = [
        ("shortest", bruteforce.shortestPaths),
        ("longest", bruteforce.longestPath),
    ]

    distLookup = {}
    for title, func in comparisons:
        paths = func(distanceMatrix)
        dist = utils.pathDistance(distanceMatrix, paths[0])
        distLookup[title] = dist
        show(title, paths, dist)

    print "Running..."

    tsp = boltzmann.TSP(distanceMatrix)
    path = tsp.solve()
    dist = utils.pathDistance(distanceMatrix, path)

    show("boltzmann", [path], dist)

    score = (1.0-(float(dist-distLookup['shortest'])/float(distLookup['longest']-distLookup['shortest']) ))

    color = bcolors.RED
    if score == 1:
        color = bcolors.GREEN
    elif score > 0.6:
        color = bcolors.YELLOW

    print "%sScore (out of 1, higher is better):%s %s%2.2f%s" % (bcolors.HEADER, bcolors.NORMAL, color, score, bcolors.NORMAL)
