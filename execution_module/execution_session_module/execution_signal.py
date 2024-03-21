from typing import Optional

from global_utils import GlobalComponentIDGenerator
from session import Session


class ExecutionSignal(Session):

    def __init__(self):
        super().__init__()
        self._id: str = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self._signal_name: Optional[str] = None
        self._msd: Optional[int] = None

    @property
    def msd(self) -> int:
        return self._msd

    @msd.setter
    def msd(self, value: int):
        self._msd = value

    @property
    def signal_name(self) -> str:
        return self._signal_name

    def refresh_status(self):
        raise NotImplementedError

    def is_completed(self):
        raise NotImplementedError
