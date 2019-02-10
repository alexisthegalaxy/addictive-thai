class A(object):
    def __init__(self):
        self.value = 10

class B(object):
    def __init__(self):
        self.a: A = None

a = A()
b = B()
b.a = a
a.value = 10000
print(b.a.value)
