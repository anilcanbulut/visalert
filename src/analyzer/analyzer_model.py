from abc import ABC, abstractmethod

class AnalyzerModel(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def analyze(self, data:list[str]) -> str:
        raise NotImplementedError("Subclasses must implement this method")