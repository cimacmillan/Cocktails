from typing import Callable

from src.indicators.GradientCoefficient import GradientCoefficient
from src.indicators.NormalisedSMA import NormalisedSMA
from dataclasses import dataclass
import backtrader as bt

@dataclass
class NeuralModel:
    layers: [int]
    indicators: [Callable]




