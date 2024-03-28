from abc import ABC, abstractmethod


class DataSession(ABC):
    """
    TODO: add abstract methods for data session
    """

    @abstractmethod
    def get_session_type(self):
        pass

    @abstractmethod
    def close(self):
        pass