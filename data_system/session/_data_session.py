from typing import Optional

from .._enums import OperationMode
from utils.global_id import GlobalComponentIDGenerator


class DataSession:
    def __init__(self):
        self._id = GlobalComponentIDGenerator.generate_unique_id(
            self.__class__.__name__, id(self)
        )
        self._session_type: Optional[OperationMode] = None

    @property
    def session_type(self):
        return self._session_type

    @property
    def id(self):
        return self._id

    def close(self):
        pass
