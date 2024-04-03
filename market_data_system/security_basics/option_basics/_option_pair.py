from typing import Optional

from .core import Put, Call
from ..._enums import OptionType


class OptionPair:
    def __init__(self, strike: int, expiration: int, put: Optional[Put] = None, call: Optional[Call] = None):
        if not isinstance(strike, int):
            raise ValueError("Strike must be an integer")
        if not isinstance(expiration, int):
            raise ValueError("Expiration must be an integer")
        self._strike = strike
        self._expiration = expiration
        if put is not None and put.type != OptionType.PUT:
            raise ValueError("Put option type is not PUT")
        if call is not None and call.type != OptionType.CALL:
            raise ValueError("Call option type is not CALL")
        self._put = put
        self._call = call

    @property
    def put(self):
        return self._put

    @property
    def call(self):
        return self._call

    @put.setter
    def put(self, put: Put):
        if self._put.type != OptionType.PUT:
            raise ValueError("Put option type is not PUT")
        self._put = put
    @call.setter
    def call(self, call: Call):
        if self._call.type != OptionType.CALL:
            raise ValueError("Call option type is not CALL")
        self._call = call

    @property
    def strike(self):
        return self._strike

    def get_option(self, option_type: OptionType | str):
        if isinstance(option_type, str):
            option_type = OptionType.get_option_type(option_type)

        match option_type:
            case OptionType.PUT:
                return self._put
            case OptionType.CALL:
                return self._call
            case _:
                raise ValueError("Invalid option type")


