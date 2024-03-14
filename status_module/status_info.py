from enum import Enum


class StatusInfo:
    def __init__(self, status: Enum, **kwargs):
        self.status = status
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        attributes = ', '.join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"StrategySectionStatusInfo({attributes})"

    def __str__(self):
        return self.__repr__()