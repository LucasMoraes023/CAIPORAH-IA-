from abc import ABC, abstractmethod

class Engine(ABC):
    @abstractmethod
    def start(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def stop(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def status(self) -> str:
        raise NotImplementedError
