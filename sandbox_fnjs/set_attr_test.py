class MyClass:
    def __init__(self):
        self.attribute = None

# Creating an instance of MyClass
obj = MyClass()

# Initially, attribute is None
print(f"Initial attribute value: {obj.attribute}")

# Using setattr to change the value of 'attribute'
setattr(obj, 'attribute', '123')

# Now, attribute has a new value
print(f"New attribute value: {obj.attribute}")
