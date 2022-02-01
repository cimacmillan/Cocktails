import sys
import threading
from copy import deepcopy
import random
from statistics import mean

import backtrader
import numpy as np

from src.model.ExperimentSet import ExperimentSet, SEEDS, ExperimentResult, EXPERIMENTS
from src.model.NeuralNetworkFactory import saveNetwork, loadNetwork, createRandomNetwork
from src.model.TrainSet import TrainSet, TrainResult
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
    endingValue = cerebro.broker.getvalue()
    percentageReturn = endingValue
    # print("Return for", params, " = ", percentageReturn)
    return (results[0].analyzers.getbyname("trades").get_analysis(), percentageReturn, cerebro)

def getNetProfit(analysis):
    try:
        return analysis["pnl"]["net"]["total"]
    except:
        return 0


def getOrderedCohort(cohort, getIndicators):
    result = []
    for network in cohort:
        params = dict(
            network=network,
            getIndicators=getIndicators
        )
        (analysis, percentageReturn, _) = backtestStrategy(NeuralGradient, params)
        score = percentageReturn
        tradeCount = analysis["total"]["total"]
        result.append((score, network))
        # print(analysis)
        print("- Score:", score, "- Trades", tradeCount, " - Profit:", getNetProfit(analysis))
    result.sort(key=lambda x: x[0], reverse=True)
    return result


NEW_NETWORKS = 5
MUTATED_NETWORKS = 15
COPY_NETWORK = 5
COHORT_SIZE = NEW_NETWORKS + MUTATED_NETWORKS + COPY_NETWORK + 1
WEIGHT_MUTATE_RATE = 0.5
ACTIVATION_MUTATE_RATE = 0.05
GENERATIONS = 1000
STAGNANT = 20

def getMutatedNetwork(random, network, trainSet, interpolation):
    linearMutation = trainSet.linearMutation
    copy = deepcopy(network)
    if linearMutation:
        weightInterp = interpolation * WEIGHT_MUTATE_RATE
        weightAntiInterp = 1 - weightInterp
        actInterp = interpolation * ACTIVATION_MUTATE_RATE
        actAntiInterp = 1 - actInterp
        for x in range(len(copy.weights)):
            weightMatrix = copy.weights[x]
            randomWeights = (random.rand(*weightMatrix.shape) - 0.5) * 2
            copy.weights[x] = (weightMatrix * weightAntiInterp) + (randomWeights * weightInterp)

        for x in range(len(copy.activations)):
            activationMatrix = copy.activations[x]
            randomActivations = (random.rand(*activationMatrix.shape) - 0.5) * 2
            copy.activations[x] = (activationMatrix * actAntiInterp) + (randomActivations * actInterp)
    else:
        for x in range(len(copy.weights)):
            weightMatrix = copy.weights[x]
            randomWeights = (random.rand(*weightMatrix.shape) - 0.5) * WEIGHT_MUTATE_RATE
            copy.weights[x] += randomWeights

        for x in range(len(copy.activations)):
            activationMatrix = copy.activations[x]
            randomActivations = (random.rand(*activationMatrix.shape) - 0.5) * ACTIVATION_MUTATE_RATE
            copy.activations[x] += randomActivations
    return copy

def getNewCohort(random, orderedCohort, trainSet):
    newCohort = [orderedCohort[0][1]]
    for x in range(MUTATED_NETWORKS):
        interp = x / MUTATED_NETWORKS
        newCohort.append(getMutatedNetwork(random, orderedCohort[0][1], trainSet, interp))

    for x in range(COPY_NETWORK):
        interp = x / COPY_NETWORK
        newCohort.append(getMutatedNetwork(random, orderedCohort[x + 1][1], trainSet, interp))

    for x in range(NEW_NETWORKS):
        newCohort.append(createRandomNetwork(random, trainSet.model.layers))

    return newCohort

def train(trainSet, trainResult, random):
    previousScore = None
    stagnantGenerations = 0
    cohort = [createRandomNetwork(random, trainSet.model.layers) for x in range(COHORT_SIZE)]
    for x in range(GENERATIONS):
        orderedCohort = getOrderedCohort(cohort, trainSet.model.indicators)
        print(trainSet.name, "Generation ", x, " Best: ", orderedCohort[0][0])
        saveNetwork(trainSet.name + "_cache", orderedCohort[0][1])
        cohort = getNewCohort(random, orderedCohort, trainSet)
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
    saveNetwork(trainSet.name, cohort[0])
    print("Saved")
    trainResult.score = previousScore

def executeExperiment(a):
    results = []
    threads = []
    for x in SEEDS:
        rs = np.random.RandomState(x)
        trainSet = TrainSet(
            model=a.model,
            name=a.name + "_" + str(x),
            linearMutation=a.linearMutation
        )
        trainResult = TrainResult(score=-1)
        x = threading.Thread(target=train, args=(trainSet, trainResult, rs))
        threads.append(x)
        results.append(trainResult)
        x.start()

    for x in threads:
        x.join()

    scores=[]

    for x in results:
        scores.append(x.score)

    return ExperimentResult(
        scores=scores,
        overallScore=mean(scores),
        name=a.name
    )


def experiment(experiments):
    results = []
    for experiment in experiments:
        results.append(executeExperiment(experiment))

    print("Results")
    for result in results:
        print(result)



print("Start with args", sys.argv)

LIVE = "live"
TRAIN = "train"
EXPERIMENT = "experiment"


if sys.argv.__contains__(LIVE):
    print("Executing live")
    network = loadNetwork("test", EXPERIMENTS[0].model.layers)
    params = dict(
        network=network,
        getIndicators=EXPERIMENTS[0].model.indicators
    )
    executeStrategyLive(NeuralGradient, params)
elif sys.argv.__contains__(TRAIN):
    print("Executing train")
    trainResult = TrainResult(
        score=0
    )
    train(TrainSet(
        model=EXPERIMENTS[0].model,
        name="Train",
        linearMutation=EXPERIMENTS[0].linearMutation
    ), trainResult, np.random.RandomState())
elif sys.argv.__contains__(EXPERIMENT):
    print("Executing experiment")
    experiment(EXPERIMENTS)
else:
    print("Executing backtest")
    network = loadNetwork("test", EXPERIMENTS[0].model.layers)
    params = dict(
        network=network,
        getIndicators=EXPERIMENTS[0].model.indicators
    )
    (analysis, percentageReturn, cerebro) = backtestStrategy(NeuralGradient, params)
    print("Return is", percentageReturn, "Analysis is", analysis)
    cerebro.plot()


