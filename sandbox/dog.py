# dog.py
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from person import Person

class Dog:
    def __init__(self, name: str):
        self.name = name
        self.owner: 'Person' = None

    def set_owner(self, owner: 'Person'):
        self.owner = owner

    def bark(self) -> str:
        return f"{self.name} says Woof!"

    def speak(self) -> str:
        if self.owner:
            return f"I'm {self.name}, and my owner is {self.owner.name}."
        else:
            return "I'm {self.name}, and I don't have an owner."
