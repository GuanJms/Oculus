from enum import Enum, auto


class ActionStatus(Enum):
    """
    PENDING: The action has been identified but has not yet been initiated.
    EXECUTED: The action was successfully completed. All criteria were met, and the intended effect was achieved.
    FAILED: The action was attempted but did not complete successfully.
    SKIPPED: The action was deliberately not executed.
    INVALID: The action was found to be invalid or not feasible.
    """
    PENDING = auto()
    EXECUTED = auto()
    FAILED = auto()
    SKIPPED = auto()
    INVALID = auto()
