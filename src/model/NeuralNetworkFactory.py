import numpy as np

from src.model.NeuralNetwork import NeuralNetwork

SAVE_DIR = "train/"

def saveNetwork(title, network):
    for x in range(len(network.weights)):
        np.savetxt(SAVE_DIR + title + "weights" + str(x), network.weights[x])
    for y in  range(len(network.activations)):
        np.savetxt(SAVE_DIR + title + "activations" + str(y), network.activations[y])

def loadNetwork(title, layers):
    weights = []
    activations = []
    for x in range(len(layers) - 1):
        weights.append(np.loadtxt(SAVE_DIR + title + "weights" + str(x)))
        activations.append(np.loadtxt(SAVE_DIR + title + "activations" + str(x)))

    return NeuralNetwork(layers, weights, activations)

def createRandomNetwork(random, layers, weightScale = 1, activationScale = 1):
    weights = []
    activations = []
    for x in range(len(layers) - 1):
        inputSize = layers[x]
        outputSize = layers[x + 1]
        weights.append(
            (random.rand(outputSize, inputSize) - 0.5) * 2 * weightScale
        )
        activations.append(
            (random.rand(layers[x + 1]) - 0.5) * 2 * activationScale
        )

    return NeuralNetwork(layers, weights, activations)


