import numpy as np

class NeuralNetwork:
    def __init__(self, layers, weights, activations):
        self.values = list(map(
            lambda x: np.zeros(x),
            layers
        ))
        print(self.values)

    def output(self):
        print("Output test")



