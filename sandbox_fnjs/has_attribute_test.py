import inspect

def custom_hasattr(obj, attr):
    return attr in obj.__dir__()

class testClassA:

    def __init__(self):
        self.triangle = "triangle"
        self._random = "random"

    def name(self):
        return "testClassA"

    def _send(self):
        return "send"