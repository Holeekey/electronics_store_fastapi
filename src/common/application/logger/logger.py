from abc import ABC, abstractmethod


class ILogger(ABC):
    
    @abstractmethod
    def log(self, *args) -> None:
        pass
    
    @abstractmethod
    def error(self, *args) -> None:
        pass
    
    @abstractmethod
    def exception(self, *args) -> None:
        pass
    