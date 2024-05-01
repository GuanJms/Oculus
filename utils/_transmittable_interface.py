from abc import ABC, abstractmethod
from typing import Any


class _TimeStampedTransmittable(ABC):
    @abstractmethod
    def send_timestamp(self):
        pass

    @abstractmethod
    def receive_timestamp(self, time: Any):
        pass


class _EventTransmittable(ABC):
    @abstractmethod
    def send_event(self, receiver: "_EventTransmittable", event: Any, event_data: Any):
        pass

    @abstractmethod
    def receive_event(self, event: Any, event_data: Any):
        pass


class _EventSubscriber(ABC):
    @abstractmethod
    def receive_event(self, event: Any, event_data: Any):
        pass


class _EventPublisher(ABC):
    @abstractmethod
    def publish(self, event: Any, event_data: Any):
        pass

    @abstractmethod
    def add_subscriber(self, subscriber: "_EventSubscriber"):
        pass

    @abstractmethod
    def delete_subscriber(self, subscriber: "_EventSubscriber"):
        pass
