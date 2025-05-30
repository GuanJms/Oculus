from abc import ABC, abstractmethod

class Rule(ABC):
    @abstractmethod
    def execute(self):
        """Method that should do something when implemented by a subclass."""
        pass

    @abstractmethod
    def get_param(self):
        pass

    @abstractmethod
    def add_param(self, rule_name: str, rule_param: dict):
        pass

    @abstractmethod
    def _update_rule_param(self):
        pass

    @abstractmethod
    def get_id(self):
        pass

    def get_var(self, var_name: str):
        return getattr(self, var_name, None)

# Uncomment the lines below to test the Executable interface with a subclass.
# class Rule(Executable):
#     def execute(self):
#         print("Task executed.")

# if __name__ == "__main__":
#     task = Task()
#     task.execute()
