from src.indicators.GradientCoefficient import GradientCoefficient
from src.indicators.NormalisedSMA import NormalisedSMA

MODELS = {
    "test": {
        "layers": [4, 4, 1],
        "indicators": lambda data : [
            NormalisedSMA(data, period=8),
            NormalisedSMA(data, period=16),
            NormalisedSMA(data, period=32),
            NormalisedSMA(data, period=64),
        ]
    },
    "neural_indicators": {
        "layers": [8, 8, 1],
        "indicators": lambda data : [
            GradientCoefficient(data, n=1),
            GradientCoefficient(data, n=2),
            GradientCoefficient(data, n=3),
            GradientCoefficient(data, n=5),
            GradientCoefficient(data, n=8),
            GradientCoefficient(data, n=13),
            GradientCoefficient(data, n=21),
            GradientCoefficient(data, n=34)
        ]
    }
}


