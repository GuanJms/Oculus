import unittest

from sandbox.circular_arraylist._circular_arraylist import CircularArrayList
from data_system.data_structure import FixedSizeDeque


class MyCircularArrayList(unittest.TestCase):
    def test_understanding_helper(self):
        print("\n\n" + "=" * 50)
        c = CircularArrayList()
        c.append(1)
        print(c)
        c.append(2)
        print(c)
        c.append(3)
        print(c)
        c.append(4)
        print(c)
        c.append(5)
        print(c)

        print(c.get(0))
        print(c.get(1))
        print(c.get(2))
        print(c.get(3))
        print(c.get(4))

        print(c)
        for _ in range(5):
            p = c.pop_left()
            print(p)
            print(c)

        for j in range(10):
            c.append(j)
            print(c)

    def test_fixed_circular_arraylist(self):
        print("\n\n" + "=" * 50)
        c = FixedSizeDeque(10)
        c.append(1)
        print(c)
        c.append(2)
        print(c)
        c.append(3)
        print(c)
        c.append(4)
        print(c)
        c.append(5)
        print(c)

        print(c.get(0))
        print(c.get(1))
        print(c.get(2))
        print(c.get(3))
        print(c.get(4))

        for j in range(100):
            p = c.append(j)
            print("removed element:", p)
            print("current", c)


if __name__ == "__main__":
    unittest.main()
