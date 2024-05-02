class ClassA:
    class_var = 'ClassA class_var'
    def __init__(self):
        self.instance_var = 'A instance_var'

    def instance_method(self):
        print(self.instance_var + ' instance_method' + ' ' + ClassA.class_var)


class ClassAa(ClassA):


    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(ClassAa, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self.instance_var = 'Aa instance_var'


class ClassAb(ClassA):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(ClassAb, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self.instance_var = 'Ab instance_var'


a = ClassA()
a2 = ClassA()
aa = ClassAa()
aa2 = ClassAa()
ab = ClassAb()
ab2 = ClassAb()

a.instance_method()
aa.instance_method()
ab.instance_method()

print("ID a: ", id(a))
print("ID a2: ", id(a2))
print("ID aa: ", id(aa))
print("ID aa2: ", id(aa2))
print("ID ab: ", id(ab))
print("ID ab2: ", id(ab2))
