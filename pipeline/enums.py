from enum import Enum


class PipelineStatusType(str, Enum):
    """
    Representing what status Pipeline is in
    """

    PROCESSING = "PROCESSING"
    ERROR = "ERROR"
    SUCCESS_END = "SUCCESS_END"
    UNINITIATED = "UNINITIATED"
    IDLE = "IDLE"

    def is_running(self) -> bool:
        if self.value == self.PROCESSING:
            return True
        return False

    def is_initiated(self) -> bool:
        if self.value == self.UNINITIATED:
            return False
        return True




