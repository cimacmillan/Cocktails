from dataclasses import dataclass

from src.model import NeuralModel

@dataclass
class TrainSet():
    name: str
    model: NeuralModel

@dataclass
class TrainResult():
    score: float
