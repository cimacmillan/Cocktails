from dataclasses import dataclass

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

SEEDS = [
    170319,
    351998,
    27398,
    140219,
    80820
]

EXPERIMENT_A = ExperimentSet(
    name="A",
    model=NeuralModel(
        layers=[8, 8, 1],
        indicators=lambda data: [
            GradientCoefficient(data, n=1),
            GradientCoefficient(data, n=2),
            GradientCoefficient(data, n=3),
            GradientCoefficient(data, n=5),
            GradientCoefficient(data, n=8),
            GradientCoefficient(data, n=13),
            GradientCoefficient(data, n=21),
            GradientCoefficient(data, n=34)
        ]
    ),
    linearMutation=True
)

EXPERIMENT_B = ExperimentSet(
    name="B",
    model=NeuralModel(
        layers=[8, 8, 1],
        indicators=lambda data : [
            GradientCoefficient(data, n=1),
            GradientCoefficient(data, n=2),
            GradientCoefficient(data, n=3),
            GradientCoefficient(data, n=5),
            GradientCoefficient(data, n=8),
            GradientCoefficient(data, n=13),
            GradientCoefficient(data, n=21),
            GradientCoefficient(data, n=34)
        ]
    ),
    linearMutation=False
)