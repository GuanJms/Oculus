import unittest
import time

from data_system.data_structure.deque.time_deque import TimeDeque
from sandbox.circular_arraylist.time_deque_list_implementation import TimeDequeList
from sandbox.circular_arraylist.node_time_deque import NodeTimeDeque

import random


def generate_price_around_100():
    # Generating a price using a normal distribution centered at 100 with a standard deviation of 10
    price = random.normalvariate(100, 10)
    return round(price, 2)


def generate_ps(arg_n):
    # Generating a price using a normal distribution centered at 100 with a standard deviation of 10
    ps = {}
    for i in range(arg_n):
        price = random.normalvariate(100, 10)
        p = round(price, 2)
        ps["price_" + str(i)] = p
    return ps


class Node:
    """Testing purposes only"""

    def __init__(self, value, timestamp, **kwargs):
        self._value = value
        self._timestamp = timestamp
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def value(self):
        return self._value

    @property
    def timestamp(self):
        return self._timestamp

    # def __str__(self):
    #     return f"({self._value}, {self._timestamp})"
    def __str__(self):
        return f"{self._value , self._timestamp}"

    def __repr__(self):
        return self.__str__()

    def pop(self):
        return_dict = {}
        for k, v in self.__dict__.items():
            return_dict[k] = v
            setattr(self, k, None)
        return return_dict

    def set(self, params):
        self._value = params.get("value", None)
        self._timestamp = params.get("timestamp", None)
        for k, v in params.items():
            if k not in ["value", "timestamp"]:
                setattr(self, k, v)


class NodeFactory:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(NodeFactory, cls).__new__(cls)
        return cls._instance

    def create(value=None, timestamp=None):
        return Node(value, timestamp)


class NodeFactoryV1:
    @staticmethod
    def create(value=None, timestamp=None):
        return Node(value, timestamp)


class TestTimeDeque(unittest.TestCase):
    def test_init(self):
        c = TimeDeque(10, "ms")
        self.assertEqual(str(c._unit), "MILLISECOND")
        self.assertEqual(c._max_time, 10)

    def test_has_elements_to_remove(self):
        c = TimeDeque(10, "ms")
        c.set_display_sequential(True)
        end_time = 500
        vs = []

        for ms in range(0, end_time, 1):
            p = generate_price_around_100()
            vs.append(Node().set(value=p, timestamp=ms))
            pop_v = c.append(Node(p, ms))
            # print("Removed: ", pop_v)
            print(c)

    def test_list_performance(self):
        operations_count = 1000
        max_len = 100

        test_data = TimeDequeList(max_len, "ms")
        # Timing append operation
        start_time = time.perf_counter()
        for i in range(operations_count):
            p = generate_price_around_100()
            new_node = Node(p, i)
            test_data.append(new_node)
            print(test_data)
        total_time1 = time.perf_counter() - start_time

        print("Total time (List): ", total_time1)
        #
        test_data = TimeDeque(max_len, "ms")
        # test_data.set_display_sequential(True)
        # Timing append operation
        start_time2 = time.perf_counter()
        for i in range(operations_count):
            p = generate_price_around_100()
            new_node = Node(p, i)
            test_data.append(new_node)
            print(test_data)
        total_time2 = time.perf_counter() - start_time2
        print("Total time: ", total_time2)
        print("Difference: ", total_time1 - total_time2)

    def test_factory_instance_vs_class(self):
        operations_count = 1000000
        factory = NodeFactory()
        max_len = 1000
        ps = [generate_price_around_100() for _ in range(operations_count)]
        c1 = TimeDeque(max_len, "ms")
        c1.set_display_sequential(True)
        start_time = time.perf_counter()
        for i in range(operations_count):
            node = factory.create()
            node.set(value=ps[i], timestamp=i)
            remove = c1.append(node)

        total_time1 = time.perf_counter() - start_time
        print("Total time: ", total_time1)

        c1 = TimeDeque(max_len, "ms")
        c1.set_display_sequential(True)
        start_time = time.perf_counter()
        for i in range(operations_count):
            node = NodeFactoryV1.create()
            node.set(value=ps[i], timestamp=i)
            remove = c1.append(node)
        total_time1 = time.perf_counter() - start_time
        print("Total time: ", total_time1)

    def test_node_reallocation_test(self):
        operations_count = 100
        max_len = 10
        more_args = [generate_ps(10) for _ in range(operations_count)]
        ps = [generate_price_around_100() for _ in range(operations_count)]
        c1 = TimeDeque(max_len, "ms")
        c1.set_display_sequential(True)
        start_time = time.perf_counter()
        for i in range(operations_count):
            node = NodeFactory.create()
            params = {
                "value": ps[i],
                "timestamp": i,
                **more_args[i]
            }
            node.set(params)
            remove = c1.append(node)
            # print(c1)
            # print(remove)
        total_time1 = time.perf_counter() - start_time
        print("Total time: ", total_time1)
        #
        c2 = NodeTimeDeque(max_len, "ms")
        c2.set_node_factory(NodeFactory)
        c2.set_display_sequential(True)
        start_time2 = time.perf_counter()
        for i in range(operations_count):
            params = {
                "value": ps[i],
                "timestamp": i,
                **more_args[i]
            }
            remove = c2.append(params)
            print(c2)
            # print(remove)
        total_time2 = time.perf_counter() - start_time2
        print("Total time: ", total_time2)
        print("Difference: ", total_time1 - total_time2)
        print(c2.get(0).__dict__)


if __name__ == "__main__":
    unittest.main()
