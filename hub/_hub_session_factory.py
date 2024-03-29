"""
This class is factory that builds hub sessions.
"""
from hub._enums import HubType
from hub._hub_session import HubSession


class HubSessionFactory:

    instance = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls._instance = super(HubSessionFactory, cls).__new__(cls)
        return cls.instance

    def create(self, hub_type: HubType, **kwargs) -> HubSession:
        match hub_type:
            case HubType.BACKTESTING:
            hub_session = HubSession()


