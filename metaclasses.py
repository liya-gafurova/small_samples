import datetime
import random
from functools import wraps
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


# while True:
#     number = input('Enter number: ')
#     func = random.choice(funcs)
#     result = func(int(number))
#     print(f'Result is: {result}\n\n')


##################################################
#             decorators with params             #
##################################################
def cached(limit: int = 100):
    def decorator(func):
        _cache = {}

        def new_func(a: int):
            print(_cache)
            if a not in _cache:
                if len(_cache) >= limit:
                    return func(a)
                _cache[a] = func(a)
            return _cache[a]

        return new_func

    return decorator


@cached(limit=5)
def get_sqrt(a: int) -> float:
    print('Compute SQRT value...')
    return sqrt(a)


# while True:
#     number = input('Enter number: ')
#     result = get_sqrt(int(number))
#     print(f'Result is: {result}\n\n')


##################################################
#                     @wraps                     #
##################################################

def cached(limit: int = 100):
    def decorator(func):
        _cache = {}

        @wraps(func)
        def new_func(a: int):
            print(_cache)
            if a not in _cache:
                if len(_cache) >= limit:
                    return func(a)
                _cache[a] = func(a)
            return _cache[a]

        return new_func

    return decorator


@cached(limit=5)
def get_sqrt(a: int) -> float:
    """
    :param a: number for witch SQRT value will be calculated
    :return: SQRT of a param
    """
    print('Compute SQRT value...')
    return sqrt(a)

#
# while True:
#     number = input('Enter number: ')
#     result = get_sqrt(int(number))
#     print(get_sqrt.__name__) # new_func
#     print(get_sqrt.__doc__) # None
#     print(f'Result is: {result}\n\n')


# TODO cached_property

##################################################
#                class decorators                #
##################################################

"""
class decorators can change behavior of class
"""

def cached(method):
    method._cached = True ### mark method to be cached
    return method


def actual_cache_decorator(method, cache_param_name):
    method_name = method.__name__

    def cached_method(self):
        global_cache = getattr(self, cache_param_name)

        if method_name not in global_cache:
            global_cache[method_name] = {}
        cache = global_cache[method_name]

        if self._value not in cache:
            cache[self._value] = method(self)
        return cache[self._value]

    return cached_method


def cached_methods(cache_param_name):
    def decorator(klass):
        setattr(klass, cache_param_name, {})

        for attr_name in klass.__dict__:
            attr = getattr(klass, attr_name)
            if hasattr(attr, '_cached') and attr._cached: # get marked methods
                setattr(klass, attr_name, actual_cache_decorator(attr, cache_param_name)) # set actual cache decorator
        return klass

    return decorator


@cached_methods('MY_CACHE') # define, that class may have cached methods and define name of cache param
class Number:

    def __init__(self, value):
        self._value = value

    @cached ### mark cached method
    def sqrt(self):
        return type(self)(sqrt(self._value))

    @cached ### mark cached method
    def half(self):
        return type(self)(self._value // 2)

    def __repr__(self):
        return f'Number({self._value})'

num = Number(15)
num.half()
print(num)
print(num.MY_CACHE)

##################################


def Singleton(klass: object):

    instance = None

    new_new_method = lambda meth: instance if instance else super(klass).__new__(klass)
    setattr(klass, '__new__', new_new_method)


    return klass

@Singleton
class SomeClass(object):
    def __init__(self, value):
        self._value = value


wer =SomeClass('wegw')
qw = SomeClass('wergwsetg')

