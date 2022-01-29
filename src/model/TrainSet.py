from dataclasses import dataclass

from src.model import NeuralModel

@dataclass
class TrainSet():
    name: str
    model: NeuralModel
    linearMutation: bool

@dataclass
class TrainResult():
    score: float
