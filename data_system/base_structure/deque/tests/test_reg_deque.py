import unittest
from data_system.base_structure.deque import RegulatorDeque
from data_system.base_structure.deque.regulators import StaticMaxTimeRegulator
from data_system.base_structure.deque.regulators.static_max_size_reg import StaticMaxSizeRegulator
from data_system.tracker.cores.tests.test_time_node import TestTimeNode


class TestRegulatorDeque(unittest.TestCase):
    def test_regulator_deque(self):
        d = RegulatorDeque()
        d.set_display_sequential(True)
        d.add_regulator(StaticMaxTimeRegulator(max_time=10))
        d.add_regulator(StaticMaxTimeRegulator(max_time=2))

        for i in range(20):
            node = TestTimeNode.generate_random(time=i)
            d.append(node)
            print(d)

    def test_multi_type_regulartor_deque(self):
        d = RegulatorDeque()
        d.set_display_sequential(True)
        r1 = StaticMaxTimeRegulator(max_time=10)
        d.add_regulator(r1)
        r2 = StaticMaxSizeRegulator(max_size=30)
        d.add_regulator(r2)

        for i in range(30):
            node = TestTimeNode.generate_random(time=i)
            d.append(node)
            print(d)


if __name__ == "__main__":
    unittest.main()
