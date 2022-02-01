from dataclasses import dataclass

from backtrader.indicators import AccelerationDecelerationOscillator, AdaptiveMovingAverage, AroonDown, AroonOscillator, \
    AwesomeOscillator

from src.indicators.GradientCoefficient import GradientCoefficient
from src.indicators.NormalisedSMA import NormalisedSMA
from src.model.NeuralModel import NeuralModel

@dataclass
class ExperimentSet:
    name: str
    model: NeuralModel
    linearMutation: bool

@dataclass
class ExperimentResult:
    scores: [float]
    overallScore: float
    name: str

SEEDS = [
    170319,
    351998,
    27398,
    140219,
    80820
]

EXPERIMENTS = [
    ExperimentSet(
        name="A",
        model=NeuralModel(
            layers=[9, 9, 1],
            indicators=lambda data: [
                AccelerationDecelerationOscillator(data),
                NormalisedSMA(data, period=8),
                NormalisedSMA(data, period=16),
                NormalisedSMA(data, period=32),
                AroonOscillator(data),
                AwesomeOscillator(data),
                GradientCoefficient(data, n=8),
                GradientCoefficient(data, n=16),
                GradientCoefficient(data, n=32),
            ]
        ),
        linearMutation=True
    ),
    ExperimentSet(
        name="B",
        model=NeuralModel(
            layers=[9, 9, 1],
            indicators=lambda data: [
                AccelerationDecelerationOscillator(data),
                NormalisedSMA(data, period=8),
                NormalisedSMA(data, period=16),
                NormalisedSMA(data, period=32),
                AroonOscillator(data),
                AwesomeOscillator(data),
                GradientCoefficient(data, n=8),
                GradientCoefficient(data, n=16),
                GradientCoefficient(data, n=32),
            ]
        ),
        linearMutation=True
    )
]
