import utils
import numpy as np
import math
import time
import collections

class TSP:

    def __init__(self, distanceMatrix):

        self.distanceMatrix = distanceMatrix
        self.numCities = distanceMatrix.shape[0]
        self.tourSteps = self.numCities + 1
        self.numStates = self.numCities * self.tourSteps

        self.states = np.eye(self.tourSteps)
        # delete the last row, as this does not represent a city, but the last column represents the last trip back to the first node
        self.states = np.delete(self.states, self.numCities, axis=0)

        # a guiding constraint: penalty > bias >= 2 * longestDistance
        bias = 2*np.max(self.distanceMatrix)
        penalty = 2*bias  # arbitrary

        self.weights = self._initWeights(penalty, bias)
        self.temperature = self._initTemp(penalty, bias)

    def _initWeights(self, penalty, bias):
        # This is a data buffer of 900 elements (5*6*5*6), with a view (shape) defined
        # by the number of cities (5) and the number of tour steps (6) between all
        # other cities (5) and all other tours steps (6) (or a fully connected hopfield-like
        # network).
        weights = np.zeros( (self.numCities, self.tourSteps, self.numCities, self.tourSteps) )

        # The values represent the distance between the two given city indexes, evaluated
        # at the given tour steps. Furthermore, impossible configurations (such as visiting
        # two cities at the same time) or undesirable configurations (such as visiting the same
        # city twice) is penalized by assigning a high positive value at these city,tour locations
        # in the weight matrix.
        for city in range(self.numCities):
            distances = self.distanceMatrix[city, :]
            for tourStep in range(self.numCities+1):
                curWeights = weights[city, tourStep]

                # ensure that where you start doesn't matter to the overall solution
                prevTourStep = tourStep - 1 if tourStep > 0 else self.tourSteps - 1
                curWeights[:, prevTourStep] = distances

                # ensure that where you finish doesn't matter to the overall solution
                nextTourStep = tourStep + 1 if tourStep < self.tourSteps - 1 else 0
                curWeights[:, nextTourStep] = distances

                # don't visit other cities at that tour step (simultaneous visits)
                curWeights[:, tourStep] = penalty

                # don't visit the same city multiple times in a tour
                if tourStep == 0:
                    curWeights[city, :-1] = penalty
                elif tourStep == self.numCities:
                    curWeights[city, 1:] = penalty
                else:
                    curWeights[city, :] = penalty

                # benefit from visiting the city
                if tourStep == 0 or tourStep == self.numCities:
                    # taking the first step implies the last step being known
                    curWeights[city, 0] = -bias
                    curWeights[city, self.numCities] = -bias
                else:
                    curWeights[city, tourStep] = -bias
        return weights

    def _initTemp(self, penalty, bias):
        # should be generally proportional to the number of steps and total cities to visit, but also
        # ensure that the temperature starts off significantly higher than highest change in consensus that can occur
        return ((penalty * self.numCities * self.tourSteps) - bias) * 100


    def _stateProbability(self, city, tour, temperature):
        #### DELTA Consensus ###################################################

        # we are copying the state before modifying it since this is a "what if"
        # branch.... so don't affect the "real" state
        states = self.states.copy()

        # this is the weights and current state for the given city/tour step
        state = self.states[city, tour]
        weights = self.weights[city, tour]

        # "what if" we flipped the state at the given city/tour...
        states[city, tour] = (1 - state)

        # calculate the activity value with this "what if" scenario...
        weightEffect = np.sum(weights * states)
        biasEffect = weights[city, tour]
        activityValue = weightEffect + biasEffect

        # check the consensus as if we had flipped this spot in the tour...
        deltaConsensus = ((1 - state) - state) * activityValue

        #### Probability of flipping state ######################################

        # sigmoid activation function
        exponential = np.exp(-1 * deltaConsensus / temperature)
        probability = 1 / (1 + exponential)

        return probability, deltaConsensus


    def solve(self):
        lastValidState = self.states.copy()

        # just used for printing status...
        lowest_temp = 0.1
        highest_temp = self.temperature
        start = time.time()
        shortStart = None
        validHits = 0
        # {state:times explored} Note this is not used in solving, just for tracking progress
        statesExplored = collections.defaultdict(int)
        changes = 0

        # keep going until we've cooled enough...
        while self.temperature > lowest_temp:

            # just used for printing status...
            if shortStart == None:
                shortStart = time.time()

            # within each cooling epoch, keep exploring states
            for _ in range(self.numStates**2):

                # select a random city and tour
                city = np.random.random_integers(0, self.numCities-1, 1)[0]
                tour = np.random.random_integers(0, self.tourSteps-1, 1)[0]

                # delta consensus is only returned for reporting purposes
                stateProbability, deltaConsensus = self._stateProbability(city, tour, self.temperature)

                # randomly flip the state based on the state probability (simulates a
                # coinflip with a biased coin)
                if np.random.binomial(1, stateProbability) == 0:
                    changes += 1   # just used for printing status...

                    # finally! flip the state (for real)!
                    self.states[city, tour] = 1 - self.states[city, tour]

                    # if the first or last tour step was randomly selected, also flip the other.
                    if tour == 0:
                        self.states[city, self.tourSteps-1] = self.states[city, tour]
                    elif tour == self.tourSteps-1:
                        self.states[city, 0] = self.states[city, tour]

                    if utils.isPathValid(self.states):
                        lastValidState = self.states.copy()

                        # just used for printing status...
                        statesExplored[str(lastValidState)] += 1
                        validHits += 1

            # cooling...
            self.temperature *= 0.975

            # show some stats as we go (gotta know whether we should pop popcorn or not)...
            if time.time()-shortStart > 1:
                shortStart = None
                elapsed = time.time() - start
                percentEst = (math.log(((highest_temp)/(self.temperature+1)))/math.log(highest_temp))*100
                secLeft = (100*(elapsed/percentEst)-elapsed)
                if secLeft > 0:
                    m, s = divmod(secLeft, 60)
                    h, m = divmod(m, 60)
                    eta = "%d:%02d:%02d" % (h, m, s)
                else:
                    eta = "0:00:00"
                    percentEst = 100
                dist = utils.pathDistance(self.distanceMatrix, utils.path(lastValidState))
                print "Temp:%-12s  PercentComplete:%-10s  ETA:%-s    Flips:%-10s  BestDist:%-7s DeltaConsensus:%-10s ValidStates:%d/%d " % ( "%.2f"%self.temperature, "%3.2f %%"%percentEst, eta, str(changes), str(dist),  str(deltaConsensus),  len(statesExplored.values()), sum(statesExplored.values()) )
                changes = 0

        # by this point the last valid state variable should hold the results of the simulated annealing
        return utils.path(lastValidState)
