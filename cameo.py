from functools import wraps

"""
A decorator could only perform side effect operations, such as 
checking that a value exists in a global dictionary, but you
can really do anything with them, including messing with the
arguments passed to the function.

The thing is, in the case where argument order matters, you 
have to account for the fact that there's always a first 
'self' or 'cls' argument in addition to the regular args. 
This is kind of a PITA.

But what if you cloud *decorate* your decorator to abstract 
away this first parameter ? This module contains what you 
need to it.

To allow your decorator to both operate on regular functions 
and class/instance methods, just decorate it with 'cameo' 
defined down there.

"""

class Cameleon:

    def __init__(self, fun, dec):

        self.fun = fun
        self.dec = dec

        self.call = self.dec(self.fun)

        self.decorated_instances = {}

    def __call__(self, *a, **kw):
        return self.call(*a, **kw)

    def __get__(self, instance, owner):        

        ufun = self.decorated_instances.get(
            (instance, owner)
        )

        if ufun is None:
            ufun = self.dec(self.fun.__get__(instance, owner))
            self.decorated_instances[instance, owner] = ufun

        return ufun


def cameo(deco):

    """
    Enables instance & class methods support for a decorator.
    """

    @wraps(deco)
    def decoception(fun):
        return Cameleon(fun, deco)

    return decoception

# --- Test code v

@cameo
def giddy(fun):
    """
    Should print the first argument, but not 'self'.
    """
    @wraps(fun)
    def wrapper(item, *args, **kwargs):
        print('GIDDY!', item)
        return fun(item, *args, **kwargs)

    return wrapper


def allo(fun):
    """
    Should print the first argument, but not 'self'.
    """
    @wraps(fun)
    def wrapper(*args, **kwargs):
        print('ALLO ?!', fun)
        return fun(*args, **kwargs)

    return wrapper 


class A:
    def f(self, *args):
        print('A.f:', args)

    @giddy
    @allo
    def l(self, *args):
        print('A.l:', args)

@allo
@giddy
def g(*args):
    print(args)


if __name__ == "__main__":
    
    a = A()

    a.f()
    a.l(32)

    g(36)