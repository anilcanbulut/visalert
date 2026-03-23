from abc import ABC, abstractmethod

class BaseDataCollector(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def collect_data(self):
        raise NotImplementedError("Subclasses must implement this method")