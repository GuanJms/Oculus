# person.py
from typing import Optional
from dog import Dog

class Person:
    def __init__(self, name: str):
        self.name = name
        self.pet: Optional[Dog] = None

    def adopt_pet(self, pet: Dog):
        self.pet = pet
        pet.set_owner(self)

    def speak(self) -> str:
        if self.pet:
            return f"My name is {self.name}, and I have adopted {self.pet.name}."
        else:
            return f"My name is {self.name}, and I don't have a pet."
