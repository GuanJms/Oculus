from section import Section


class ExecutionSignalSection(Section):

    def __init__(self):
        super().__init__()
        raise NotImplementedError

    def refresh_status(self):
        raise NotImplementedError
