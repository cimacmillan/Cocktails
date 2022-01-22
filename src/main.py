import os
import sys
from copy import deepcopy

import numpy
import numpy as np

from src.indicators.GradientCoefficient import GradientCoefficient
from src.model.Neural import NeuralNetwork
from src.oanda.live import getLiveCerebro
from src.oanda.backtest import getBacktestCerebro
from src.strategy.NeuralGradient import NeuralGradient

def executeStrategyLive(strategy, params):
    cerebro = getLiveCerebro()
    cerebro.addstrategy(strategy, **params)
    cerebro.run(exactbars=1)


def backtestStrategy(strategy, params):
    startingValue = 100000
    cerebro = getBacktestCerebro()
    cerebro.addstrategy(strategy, **params)
    cerebro.broker.setcash(startingValue)
    cerebro.broker.setcommission(commission=0.0001)
    # print("Value before run", cerebro.broker.getvalue())
    cerebro.run()
    # print("Value after run", cerebro.broker.getvalue())
    cerebro.plot()
    endingValue = cerebro.broker.getvalue()
    percentageReturn = endingValue / startingValue
    # print("Return for", params, " = ", percentageReturn)
    return percentageReturn

MODEL = [8, 8, 1]
SAVE_DIR = "train/"

def saveNetwork(title, network):
    for x in range(len(network.weights)):
        numpy.savetxt(SAVE_DIR + title + "weights" + str(x), network.weights[x])
    for y in  range(len(network.activations)):
        numpy.savetxt(SAVE_DIR + title + "activations" + str(y), network.activations[y])

def loadNetwork(title):
    layers = MODEL
    weights = []
    activations = []
    for x in range(len(layers) - 1):
        weights.append(numpy.loadtxt(SAVE_DIR + title + "weights" + str(x)))
        activations.append(numpy.loadtxt(SAVE_DIR + title + "activations" + str(x)))

    return NeuralNetwork(layers, weights, activations)

def createRandomNetwork(layers):
    weights = []
    activations = []
    for x in range(len(layers) - 1):
        inputSize = layers[x]
        outputSize = layers[x + 1]
        weights.append(
            (np.random.rand(outputSize, inputSize) - 0.5) * 100
        )

        activations.append(
            (np.random.rand(layers[x + 1]) - 0.5) / 100
        )

    return NeuralNetwork(layers, weights, activations)


def getIndicators(data):
    return [
        GradientCoefficient(data, n=1),
        GradientCoefficient(data, n=2),
        GradientCoefficient(data, n=3),
        GradientCoefficient(data, n=5),
        GradientCoefficient(data, n=8),
        GradientCoefficient(data, n=13),
        GradientCoefficient(data, n=21),
        GradientCoefficient(data, n=34)
    ]


def getNetworkScore(network):
    params = dict(
        network=network,
        getIndicators=getIndicators
    )
    return backtestStrategy(NeuralGradient, params)


def getOrderedCohort(cohort):
    result = []
    for network in cohort:
        score = getNetworkScore(network)
        result.append((score, network))
        print("- Score: ", score)

    result.sort(key=lambda x: x[0], reverse=True)
    return result


NEW_NETWORKS = 5
MUTATED_NETWORKS = 5
COPY_NETWORK = 5
COHORT_SIZE = NEW_NETWORKS + MUTATED_NETWORKS + COPY_NETWORK + 1
cohort = [createRandomNetwork(MODEL) for x in range(COHORT_SIZE)]
WEIGHT_MUTATE_RATE = 1
ACTIVATION_MUTATE_RATE = 1 / 100
GENERATIONS = 100

def getMutatedNetwork(network):
    copy = deepcopy(network)
    for x in range(len(copy.weights)):
        weightMatrix = copy.weights[x]
        randomWeights = (np.random.random(weightMatrix.shape) - 0.5) * WEIGHT_MUTATE_RATE
        copy.weights[x] += randomWeights

    for x in range(len(copy.activations)):
        activationMatrix = copy.activations[x]
        randomActivations = (np.random.random(activationMatrix.shape) - 0.5) * ACTIVATION_MUTATE_RATE
        copy.activations[x] += randomActivations
    return copy

def getNewCohort(orderedCohort):
    newCohort = [orderedCohort[0][1]]
    for x in range(MUTATED_NETWORKS):
        newCohort.append(getMutatedNetwork((orderedCohort[0][1])))

    for x in range(COPY_NETWORK):
        newCohort.append(getMutatedNetwork(orderedCohort[x + 1][1]))

    for x in range(NEW_NETWORKS):
        newCohort.append(createRandomNetwork(MODEL))

    return newCohort

print("Start with args", sys.argv)

LIVE = "live"
TRAIN = "train"


if sys.argv.__contains__(LIVE):
    print("Executing live")
    network = loadNetwork("test")
    params = dict(
        network=network,
        getIndicators=getIndicators
    )
    executeStrategyLive(NeuralGradient, params)
elif sys.argv.__contains__(TRAIN):
    for x in range(GENERATIONS):
        orderedCohort = getOrderedCohort(cohort)
        print("Generation ", x, " Best: ", orderedCohort[0][0])
        cohort = getNewCohort(orderedCohort)

    print("Best after ", GENERATIONS, " Generations")
    saveNetwork("test", cohort[0])
    print("Saved")
else:
    print("Executing backtest")
    network = loadNetwork("test")
    params = dict(
        network=network,
        getIndicators=getIndicators
    )
    percentageReturn = backtestStrategy(NeuralGradient, params)
    print("Return is", percentageReturn)

