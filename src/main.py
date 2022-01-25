import sys
from copy import deepcopy

import backtrader
import numpy as np

from src.model.NeuralIndicators import MODELS
from src.model.NeuralNetworkFactory import saveNetwork, loadNetwork, createRandomNetwork
from src.oanda.live import getLiveCerebro
from src.oanda.factory import getBacktestCerebro
from src.strategy.Neural import NeuralGradient

def executeStrategyLive(strategy, params):
    cerebro = getLiveCerebro()
    cerebro.addstrategy(strategy, **params)
    cerebro.run(exactbars=1)


def backtestStrategy(strategy, params):
    startingValue = 100000
    cerebro = getBacktestCerebro()
    cerebro.addstrategy(strategy, **params)
    cerebro.addanalyzer(backtrader.analyzers.TradeAnalyzer, _name = "trades")
    cerebro.broker.setcash(startingValue)
    cerebro.broker.setcommission(commission=0.0001)
    # print("Value before run", cerebro.broker.getvalue())
    results = cerebro.run()
    # print("Value after run", cerebro.broker.getvalue())
    # cerebro.plot()
    endingValue = cerebro.broker.getcash()
    percentageReturn = endingValue / startingValue
    # print("Return for", params, " = ", percentageReturn)
    return (results[0].analyzers.getbyname("trades").get_analysis(), percentageReturn, cerebro)


def getNetworkAnalysis(network, getIndicators):
    params = dict(
        network=network,
        getIndicators=getIndicators
    )
    return backtestStrategy(NeuralGradient, params)

def getNetProfit(analysis):
    try:
        return analysis["pnl"]["net"]["total"]
    except:
        return 0


def getOrderedCohort(cohort, getIndicators):
    result = []
    for network in cohort:
        (analysis, percentageReturn, _) = getNetworkAnalysis(network, getIndicators)
        score = getNetProfit(analysis)
        tradeCount = analysis["total"]["total"]
        result.append((score, network))
        # print(analysis)
        print("- Score:", score, "- Trades", tradeCount, " - Profit:", getNetProfit(analysis))
    result.sort(key=lambda x: x[0], reverse=True)
    return result


NEW_NETWORKS = 0
MUTATED_NETWORKS = 10
COPY_NETWORK = 5
COHORT_SIZE = NEW_NETWORKS + MUTATED_NETWORKS + COPY_NETWORK + 1
WEIGHT_MUTATE_RATE = 0.1
ACTIVATION_MUTATE_RATE = 0.1
GENERATIONS = 1000
STAGNANT = 20

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
        newCohort.append(createRandomNetwork(MODELS["test"]["layers"]))

    return newCohort

def train(name):
    previousScore = None
    stagnantGenerations = 0
    cohort = [createRandomNetwork(MODELS["test"]["layers"]) for x in range(COHORT_SIZE)]
    for x in range(GENERATIONS):
        orderedCohort = getOrderedCohort(cohort, MODELS["test"]["indicators"])
        print("Generation ", x, " Best: ", orderedCohort[0][0])
        saveNetwork(name + "_cache", orderedCohort[0][1])
        cohort = getNewCohort(orderedCohort)
        if previousScore is None:
            previousScore = orderedCohort[0][0]
        elif previousScore == orderedCohort[0][0]:
            stagnantGenerations = stagnantGenerations + 1
            if stagnantGenerations >= STAGNANT:
                print("Finishing early from stagnation")
                break
        else:
            stagnantGenerations = 0
            previousScore = orderedCohort[0][0]

    print("Best after ", GENERATIONS, " Generations")
    saveNetwork(name, cohort[0])
    print("Saved")

print("Start with args", sys.argv)

LIVE = "live"
TRAIN = "train"


if sys.argv.__contains__(LIVE):
    print("Executing live")
    network = loadNetwork("test", MODELS["test"]["layers"])
    params = dict(
        network=network,
        getIndicators=MODELS["test"]["indicators"]
    )
    executeStrategyLive(NeuralGradient, params)
elif sys.argv.__contains__(TRAIN):
    print("Executing train")
    train("test")
else:
    print("Executing backtest")
    network = loadNetwork("test", MODELS["test"]["layers"])
    params = dict(
        network=network,
        getIndicators=MODELS["test"]["indicators"]
    )
    (analysis, percentageReturn, cerebro) = backtestStrategy(NeuralGradient, params)
    print("Return is", percentageReturn, "Analysis is", analysis)
    cerebro.plot()


