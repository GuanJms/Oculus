from session import Session


class ExecutionAction(Session):

    def __init__(self):
        super().__init__()
        raise NotImplementedError

    def refresh_status(self):
        raise NotImplementedError

    def is_completed(self):
        raise NotImplementedError
