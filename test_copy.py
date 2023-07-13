import copy

class Data:
    def __init__(self, value):
        self.value = value


class State:

    def __init__(self):

        self.a = Data(1)
        self.b = self.a
        self.c = Data(1)


s1 = State()
s2 = State()
s3 = copy.deepcopy(s1)