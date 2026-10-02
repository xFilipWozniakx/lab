import functools
# preserving function metadata
# Normally, a function's name can be returned with the __name__ attribute:

def my_func_2():
    return "Have a great day"
print(my_func_2.__name__)


def decorator(func):
    def inner():
        return func().upper()
    return inner

# after decoration function looses its __name__ atribbute
@decorator
def my_func():
    return "Have a great day"
print(my_func.__name__)

# to fix this python has a build-in called functools.wraps that can be used to preserve the original function's name and docstring


def decorator_v2(func):
    @functools.wraps(func)
    def inner():
        return func().upper()
    return inner


@decorator_v2
def my_func_3():
    return "Have a great day"
print(my_func_3.__name__)




