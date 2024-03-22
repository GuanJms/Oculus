from enum import Enum


class ExecutionStatusType(str, Enum):
    """
    Representing what kind of status it is within Execution module
    """

    SUCCESS_END = "SUCCESS_END"
    DATA_REQUESTING = "DATA_REQUESTING"
    PROCESSING = "PROCESSING"
    ERROR = "ERROR"

    def is_ended(self) -> bool:
        if self.value == self.SUCCESS_END:
            return True
        if self.value == self.ERROR:
            return True
        return False
