from abc import ABC, abstractmethod


class DataProcessor:

    def __init__(self):
        self.calculators = []

    def add_calculator(self, calculator):
        self.calculators.append(calculator)

    def get_calculators(self):
        return self.calculators

    @abstractmethod
    def process(self, data, **kwargs):
        pass
