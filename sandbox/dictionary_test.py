dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4}

# Using another dictionary
dict1.update(dict2)
print(dict1)  # Output: {'a': 1, 'b': 3, 'c': 4}

# Using an iterable of key/value pairs
dict1.update([('b', 5), ('e', 6)])
print(dict1)  # Output: {'a': 1, 'b': 3, 'c': 4, 'd': 5, 'e': 6}