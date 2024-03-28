from enum import Enum


class ExecutionStatusType(str, Enum):
    """
    Representing what kind of status it is within Execution module
    """

    SUCCESS_END = "SUCCESS_END"
    DATA_REQUESTING = "DATA_REQUESTING"
    PROCESSING = "PROCESSING"
    ERROR = "ERROR"

    NONE_INITIATED = "NONE_INITIATED"

    def is_ended(self) -> bool:
        if self.value == self.SUCCESS_END:
            return True
        if self.value == self.ERROR:
            return True
        return False

    def is_running(self) -> bool:
        if self.value == self.DATA_REQUESTING:
            return True
        if self.value == self.PROCESSING:
            return True
        return False

    def is_data_requesting(self) -> bool:
        return self.value == self.DATA_REQUESTING
