import datetime
import random
from math import sqrt
from typing import Optional

"""
https://www.youtube.com/watch?v=CukrRuOAVqg 
https://www.youtube.com/watch?v=Rm4JP7JfsKY 

"""


###########################################################################
#                                SINGLETON                                #
###########################################################################


class Singleton:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Singleton, cls).__new__(cls)

        return cls.__instance


class Logger(Singleton):
    def write(self, msg: str):
        print(f'Logger. {datetime.datetime.now()}: {msg}')


log = Logger()
log2 = Logger()

print(log)
print(log2)


###########################################################################
#                        SINGLETON WITH METACLASS                         #
###########################################################################


class SingletonMetaclass(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SingletonMetaclass, cls).__call__(*args, **kwargs)

        return cls._instance


class Base(object, metaclass=SingletonMetaclass):
    def __new__(cls, *args, **kwargs):
        print(f'{cls.__name__}: new')
        return super(Base, cls).__new__(cls)

    def __init__(self, *args, **kwargs):
        print(f'{self.__class__.__name__}: init')

    def __call__(self, *args, **kwargs):
        print(f'{self.__class__.__name__}: call')


class Custom(Base):
    pass


c = Custom(value='some_val')
d = Custom(value='other val')

print(d)
print(c)


###########################################################################
#                        SINGLETON WITH DECORATORS                        #
###########################################################################


##################################################
#                 function logic                 #
##################################################

_sqrt_cache = {}


def get_sqrt_with_cache(a: int):
    if a not in _sqrt_cache:
        print('compute new')
        _sqrt_cache[a] = sqrt(a)

    return _sqrt_cache[a]


# while True:
#     number = input('Enter number: ')
#     result = get_sqrt_with_cache(int(number))
#     print(f'SQRT is: {result}')


##################################################
#            function with decorators            #
##################################################

def cached(func: callable):
    _cache = {}

    def new_func(a):
        if a not in _cache:
            _cache[a] = func(a)
        return _cache[a]

    return new_func


@cached
def get_sqrt(a: int) -> float:
    print('Compute SQRT value...')
    return sqrt(a)


@cached
def get_pow(a: int) -> float:
    print('Compute POW value...')
    return pow(a, 2)


funcs = [get_pow, get_sqrt]
while True:
    number = input('Enter number: ')
    func = random.choice(funcs)
    result = func(int(number))
    print(f'Result is: {result}\n\n')


##################################################
#             decorators with params             #
##################################################
