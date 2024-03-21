from abc import ABC, abstractmethod


class SignalGenerator(ABC):

    @abstractmethod
    def generate_signal(self):
        pass
