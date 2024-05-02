l1 = [1,2,3,45]
print(id(l1))
l2 = list(l1)
print(id(l2))
l1[3] = 0
print(l1, l2)