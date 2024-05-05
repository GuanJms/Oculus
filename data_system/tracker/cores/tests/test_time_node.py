import random


class TestTimeNode:
    def __init__(self, value, time):
        self.value = value
        self.timestamp = time

    def __str__(self):
        return f"({self.value}, {self.timestamp})"

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def generate_random(time=None):
        if time is not None:
            return TestTimeNode(random.random(), time)
        return TestTimeNode(random.random(), random.random())
