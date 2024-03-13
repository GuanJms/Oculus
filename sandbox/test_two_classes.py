# main.py
from person import Person
from dog import Dog

alice = Person("Alice")
buddy = Dog("Buddy")

alice.adopt_pet(buddy)

print(alice.speak())  # My name is Alice, and I have adopted Buddy.
print(buddy.speak())  # I'm Buddy, and my owner is Alice.
