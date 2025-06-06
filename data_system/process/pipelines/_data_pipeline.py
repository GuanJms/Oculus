"""
DataPiepline should be a pipeline where data processors could be added in and stack up.

Each step can have processor and process the
"""

from abc import ABC, abstractmethod
from typing import List

from data_system._enums import DomainEnum


class DataPipeline:
    _parameter_constraints: dict = {
        "steps": [list, tuple],
        "verbose": ["boolean"],
    }

    def __init__(self, steps, *, domains: List[DomainEnum] = None, verbose=False):
        self.steps = steps
        self.domains = domains
        self.verbose = verbose

    def add_step(self, step):
        self.steps.append(step)

    def process(self, data, **kwargs):
        data = data.copy()
        # self._validate_steps() # TODO: implement this
        for name, step in self.steps:
            if hasattr(step, "process"):
                data, kwargs = step.process(data, verbose=self.verbose, **kwargs)
            elif hasattr(step, "inject"):
                data, kwargs = step.inject(data, **kwargs)

    def get_step_names(self):
        return [step.name for step in self.steps]

    def find_step(self, step_name):
        for step in self.steps:
            if step.name == step_name:
                return step
        raise ValueError(f"Step {step_name} not found")

    def set_params(self, **kwargs):
        params_keys = kwargs.keys()
        # parse the parameters by the processor name follow by the parameter name
        for key in params_keys:
            processor_name, param_name = key.split("__", 1)
            processor = self.find_step(processor_name)
            processor.set_params(**{param_name: kwargs[key]})

    def _validate_steps(self):
        names, processors = zip(*self.steps)

        # validate names
        # self._validate_names(names) # TODO: implement this
        # self._validate_processors(processors) # TODO: implement this
        inter_processors = processors[:-1]
        injector = processors[-1]

        for p in inter_processors:
            if p is None or p == "passthrough":
                continue
            if not hasattr(p, "transform"):
                raise TypeError(
                    f"All intermediate steps should be transformers "
                    f"and implement transform or be the string 'passthrough' "
                    f"({hasattr(p, 'transform')} transform | "
                    f"{hasattr(p, 'inject')}). "
                    f"'{p}' (type {type(p)}) doesn't"
                )
        if (
            injector is not None
            and injector != "passthrough"
            and not hasattr(injector, "inject")
        ):
            raise TypeError(
                f"Last step of the processor should be"
                "data injector and implement inject or be the string 'passthrough'."
                f"'{injector}' (type {type(injector)}) doesn't"
            )

    def __len__(self):
        """
        Returns the length of the Pipeline
        """
        return len(self.steps)

    def __repr__(self):
        return f"DataPipeline(steps={self.steps})"
