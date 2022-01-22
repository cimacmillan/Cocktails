import numpy as np

class NeuralNetwork:
    def __init__(self, layers, weights, activations):
        self.layers = layers
        self.weights = weights
        self.activations = activations
        self.values = list(map(
            lambda x: np.zeros(x),
            layers
        ))

    def output(self, inputs):
        self.values[0] = inputs

        for layerIndex in range(0, len(self.layers) - 1):
            inputLayerIndex = layerIndex
            outputLayerIndex = layerIndex + 1
            outputLayerActivations = np.matrix(self.activations[inputLayerIndex]).transpose()
            inputLayerValues = self.values[inputLayerIndex]
            inputWeights = self.weights[inputLayerIndex]
            # print("Input weights", inputWeights, "Input layer values", inputLayerValues)
            weightedInputs = (inputWeights * inputLayerValues.transpose())
            # print("Weighted inputs", weightedInputs, "Activations", outputLayerActivations)
            withActivation = weightedInputs + outputLayerActivations
            # print("With activations", withActivation)
            self.values[outputLayerIndex] = np.arctan(withActivation).transpose()
            # print("Values", self.values[outputLayerIndex])

        return self.values[len(self.layers) - 1]



