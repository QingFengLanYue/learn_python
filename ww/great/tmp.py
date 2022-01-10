import pandas as pd


class ReadData:
    def __init__(self, file_name, **kwargs):
        self.file_name = 'data/' + file_name
        self.sep = kwargs.get('sep', False)
        self.columns = kwargs.get('columns', False)
        if self.file_name.endswith('.txt'):
            return self.read_txt(self)
        else:
            return 1

    def read_txt(self):
        reader = pd.read_csv(self.file_name, sep=self.sep, dtype=str, header=None, engine='python')
        reader.columns = self.columns
        return reader

    def read_csv(self):
        pass

    def read_excel(self):
        pass

    def read_database(self):
        pass

    def read_check(self):
        print(self.file_name)
        print(self.sep)
        print(self.columns)

        self.read_txt(self)

    # columns = ['id', 'location_id', 'node_type', 'node_code', 'parent_id', 'property_code']
    # m = read_data.read_txt('localtion.txt', '!#~', columns)


# columns = ['id', 'location_id', 'node_type', 'node_code', 'parent_id', 'property_code']
# x = ReadData('localtion.txt', sep='!#~', columns=columns)
# print(x)


import timeit


class A:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class B:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class C:
    def __init__(self, name, age):
        self.name = name
        self.age = age


def initialize_class_a():
    a = A(name="J Smith", age=20)
    b = A(name="B Jones", age=40)
    return a.name, b.name


def initialise_class_b():
    a = B(name="J Smith", age=20)
    b = B(name="B Jones", age=40)
    return a.name, b.name


def initialise_class_c():
    a = C(name="J Smith", age=20)
    b = C(name="B Jones", age=40)
    return a.name, b.name


print(initialize_class_a())
# ('J Smith', 'B Jones')
print(initialise_class_b())
# ('J Smith', 'B Jones')
print(initialise_class_c())
# ('J Smith', 'B Jones')

print(timeit.timeit("initialize_class_a()", "from __main__ import initialize_class_a"))
# 1.93
print(timeit.timeit("initialise_class_b()", "from __main__ import initialise_class_b"))
# 2.19
print(timeit.timeit("initialise_class_c()", "from __main__ import initialise_class_c"))


# 1.03
class Person(object):
    def __init__(self, name, gender, **kw):
        self.name = name
        self.gender = gender
        for k, v in kw.items():
            setattr(self, k, v)


xiaoming = Person('Xiao Ming', 'Male', birth='1990-1-1', job='Student')
print(xiaoming.name)
print(xiaoming.job)


class ExampleClass(object):
    def __init__(self, **kwargs):
        self.val = "default1"
        self.val2 = "default2"
        if "val" in kwargs:
            self.val = kwargs["val"]
            self.val2 = 2 * self.val
        elif "val2" in kwargs:
            self.val2 = kwargs["val2"]
            self.val = self.val2 / 2
        else:
            raise TypeError("must provide val= or val2= parameter values")


x = ExampleClass(val1=22, val2=15)
print(x.val, x.val2)
