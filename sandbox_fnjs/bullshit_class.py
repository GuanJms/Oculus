green = "\033[92m{}\033[0m"
red = "\033[91m{}\033[0m"
def bullshitmemory(f):
    f.__bullshit__memory__ = True
    return f


def bullshitmethod(**kwargs):
    def decorator(f):
        f.__bullshit__ = True
        f.__number__ = kwargs.get("bullshit_time", 1)
        f.__color_code__ = kwargs.get("bullshit_color_code", "\033[91m{}\033[0m")
        return f

    return decorator


def bullshitmethods(cls):
    bullshit = []
    for name, method in cls.__dict__.items():
        if getattr(method, "__bullshit__", False):
            print(method)
            bullshit.append(name)
    return bullshit


def bullshiting_methods(cls, memory):
    import random
    old_methods = {}
    new_methods = {}
    for name, method in cls.__dict__.items():
        if getattr(method, "__bullshit__", False):
            old_methods[name] = method
            bullshit_name = f"bullshit_{name}"
            new_methods[bullshit_name] = method
    for name, method in new_methods.items():
        def new_method(self, *args, method = method, **kwargs):
            for _ in range(method.__number__):
                print(method.__color_code__.format(random.choice(memory)))
            return method(self, *args, **kwargs)

        setattr(cls, name, new_method)

    for new_name, (name, method) in zip(new_methods.keys(), old_methods.items()):
        print(f"Bullshitting {name} to {new_name}")
        delattr(cls, name)


def bullshitmemorymethods(cls):
    memory = []
    for name, method in cls.__dict__.items():
        if getattr(method, "__bullshit__memory__", False):
            memory.append(name)
    return memory


class BullShitMeta(type):
    def __call__(cls, *args, **kwargs):  # called when you A()
        memory = bullshitmemorymethods(cls)
        bullshiting_methods(cls, memory)
        print(cls.__dict__)
        return super().__call__(*args, **kwargs)


class BullShitA(metaclass=BullShitMeta):
    @bullshitmemory
    def fucking_hell_no(self):
        raise PermissionError

    @bullshitmemory
    def bullshit(self):
        raise PermissionError

    @bullshitmemory
    def Iamsoooooosadrightnow(self):
        raise PermissionError

    @bullshitmemory
    def whythefuckamIdoingthis(self):
        raise PermissionError

    @bullshitmethod(bullshit_time=5)
    def ILoveHenry(self):
        print("Yoooo Henry. This method is for you????????")

    @bullshitmethod(bullshit_time=20, bullshit_color_code = green)
    def ILoveDidi(self):
        print("Yooo didi, this method is for you")

    @bullshitmethod(bullshit_time =1, bullshit_color_code = red)
    def IloveMyself(self):
        print("I Fucking hate this class")


bs_instance = BullShitA()

bs_instance.bullshit_ILoveHenry()
bs_instance.bullshit_ILoveDidi()
try:
    bs_instance.IloveMyself()
except Exception as error:
    print(error)

