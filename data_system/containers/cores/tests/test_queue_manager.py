import unittest
import random

from data_system.containers.cores.queue_manager import QueueManager
from data_system.base_structure.deque import TimeDeque
from data_system.containers.cores.tests.test_time_node import TestTimeNode


class MaxMinCalculator:
    def __init__(self):
        self._queue = []
        self._max = None
        self._min = None

    def add(self, data):
        self._queue.append(data)
        value = data.value
        if self._max is None or value > self._max:
            self._max = value
        if self._min is None or value < self._min:
            self._min = value

    def remove(self, data):
        self._queue.remove(data)
        if data.value == self._max:
            self._max = max([node.value for node in self._queue])
        if data.value == self._min:
            self._min = min([node.value for node in self._queue])

    def __str__(self):
        return f"Max: {self._max}, Min: {self._min}"

    def __repr__(self):
        return self.__str__()


class TestQueueManager(unittest.TestCase):
    def test_queue_manager_time_deque(self):
        cal_v_list = []
        cal_v_list_2 = []
        cal_v_list_3 = []
        first_10s_q = QueueManager(TimeDeque(max_time=10))
        first_10s_q._queue.set_display_sequential(True)
        min_max_calculator = MaxMinCalculator()
        first_10s_q.subscribe_to_appends(min_max_calculator)
        first_10s_q.subscribe_to_removals(min_max_calculator)

        second_10s_q = QueueManager(TimeDeque(max_time=10))
        second_10s_q._queue.set_display_sequential(True)

        min_max_calculator_2 = MaxMinCalculator()
        second_10s_q.subscribe_to_appends(min_max_calculator_2)
        second_10s_q.subscribe_to_removals(min_max_calculator_2)

        min_max_calculator_3 = MaxMinCalculator()

        first_10s_q.subscribe_to_appends(min_max_calculator_3)
        second_10s_q.subscribe_to_removals(min_max_calculator_3)

        first_10s_q.add_tail_queue(second_10s_q)

        for i in range(50):
            # generate normal distribution value
            v = random.normalvariate(100, 10)
            first_10s_q.add(TestTimeNode(v, i))
            # print("Time Node added: ", TimeNode(i, i))

            self.assertAlmostEquals(
                min_max_calculator._max,
                max([x.value for x in first_10s_q._queue._data if x]),
            )
            self.assertAlmostEquals(
                min_max_calculator._min,
                min([x.value for x in first_10s_q._queue._data if x]),
            )
            # print("second_10s_q:", second_10s_q._queue)
            # print("min_max_calculator_2:", min_max_calculator_2)
            cal_v_list.append(min_max_calculator._max)
            cal_v_list_2.append(min_max_calculator_2._max)
            cal_v_list_3.append(min_max_calculator_3._max)
        for i in range(150):
            v = random.normalvariate(100, 10)
            first_10s_q.add(TestTimeNode(v, i))
            self.assertAlmostEquals(
                min_max_calculator_2._max,
                max([x.value for x in second_10s_q._queue._data if x]),
            )
            self.assertAlmostEquals(
                min_max_calculator_2._min,
                min([x.value for x in second_10s_q._queue._data if x]),
            )
            print("first_10s_q:", first_10s_q._queue)
            print("second_10s_q:", second_10s_q._queue)
            print("min_max_calculator_2:", min_max_calculator_2)
            print("min_max_calculator:", min_max_calculator)
            print("min_max_calculator_2:", min_max_calculator_2)
            print("min_max_calculator_3:", min_max_calculator_3)
            cal_v_list.append(min_max_calculator._max)
            cal_v_list_2.append(min_max_calculator_2._max)
            cal_v_list_3.append(min_max_calculator_3._max)
        import matplotlib.pyplot as plt

        plt.plot(cal_v_list, label="Previous 2s")
        plt.plot(cal_v_list_2, label="Second 3s")
        plt.plot(cal_v_list_3, label="All seconds")
        plt.xlabel("Time")
        plt.ylabel("Max Value")
        plt.legend()
        plt.show()


if __name__ == "__main__":
    unittest.main()
