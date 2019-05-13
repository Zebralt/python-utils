
import re

# One object per function

def __add__(item): name = "__add__"; return hdecorate(item, name) # for +
def __sub__(item): name = "__sub__"; return hdecorate(item, name) # for -
def __mul__(item): name = "__mul__"; return hdecorate(item, name) # for *
def __truediv__(item): name = "__truediv__"; return hdecorate(item, name) # for /
def __floordiv__(item): name = "__floordiv__"; return hdecorate(item, name) # for //
def __mod__(item): name = "__mod__"; return hdecorate(item, name) # for %
def __pow__(item): name = "__pow__"; return hdecorate(item, name) # for **
def __and__(item): name = "__and__"; return hdecorate(item, name) # for &
def __xor__(item): name = "__xor__"; return hdecorate(item, name) # for ^
def __or__(item): name = "__or__"; return hdecorate(item, name) # for |
def __lshift__(item): name = "__lshift__"; return hdecorate(item, name) # for <<
def __rshift__(item): name = "__rshift__"; return hdecorate(item, name) # for >>
def __iadd__(item): name = "__iadd__"; return hdecorate(item, name) # for +=
def __isub__(item): name = "__isub__"; return hdecorate(item, name) # for -=
def __imul__(item): name = "__imul__"; return hdecorate(item, name) # for *=
def __idiv__(item): name = "__idiv__"; return hdecorate(item, name) # for /=
def __ifloordiv__(item): name = "__ifloordiv__"; return hdecorate(item, name) # for //=
def __imod__(item): name = "__imod__"; return hdecorate(item, name) # for %=
def __ipow__(item): name = "__ipow__"; return hdecorate(item, name) # for **=
def __ilshift__(item): name = "__ilshift__"; return hdecorate(item, name) # for <<=
def __irshift__(item): name = "__irshift__"; return hdecorate(item, name) # for >>=
def __iand__(item): name = "__iand__"; return hdecorate(item, name) # for &=
def __ixor__(item): name = "__ixor__"; return hdecorate(item, name) # for ^=
def __ior__(item): name = "__ior__"; return hdecorate(item, name) # for |=
def __neg__(item): name = "__neg__"; return hdecorate(item, name) # for –
def __pos__(item): name = "__pos__"; return hdecorate(item, name) # for +
def __abs__(item): name = "__abs__"; return hdecorate(item, name) # for abs()
def __invert__(item): name = "__invert__"; return hdecorate(item, name) # for ~
def __complex__(item): name = "__complex__"; return hdecorate(item, name) # for complex()
def __int__(item): name = "__int__"; return hdecorate(item, name) # for int()
def __long__(item): name = "__long__"; return hdecorate(item, name) # for long()
def __float__(item): name = "__float__"; return hdecorate(item, name) # for float()
def __oct__(item): name = "__oct__"; return hdecorate(item, name) # for oct()
def __hex__(item): name = "__hex__"; return hdecorate(item, name) # for hex()
def __lt__(item): name = "__lt__"; return hdecorate(item, name) # for <
def __le__(item): name = "__le__"; return hdecorate(item, name) # for <=
def __eq__(item): name = "__eq__"; return hdecorate(item, name) # for ==
def __ne__(item): name = "__ne__"; return hdecorate(item, name) # for !=
def __ge__(item): name = "__ge__"; return hdecorate(item, name) # for >=
def __gt__(item): name = "__gt__"; return hdecorate(item, name) # for >
def __matmul__(item): name = "__matmul__"; return hdecorate(item, name) # for @
def __rmatmul__(item): name = "__rmatmul__"; return hdecorate(item, name) # for @


def wushu(name):

    if not re.match(r'__[a-z]+__', name):
        name = '__%s__' % name.strip('_')

    def decorator(fun):
        return hdecorate(fun, name)
    return decorator


_memory = {}

def hdecorate(fun, operator):

    global _memory

    if isinstance(fun, X):
        fun = fun.fun
    
    decorator = _memory.get(fun, X(fun)) 
    _memory[fun] = decorator

    decorator.append(operator)

    return decorator


def _rxsable(self, name, args, kwargs):
    if name in self.ops:
        return self.fun(*args, **kwargs)
    raise TypeError('%s: this fun.operator isn\'t available, wasn\'t used as a decorator on %s'% (name, self.fun))

class X:

    def __init__(self, fun):
        self.fun = fun
        self.ops = set()

    def append(self, op):
        self.ops.add(op)

    def __hash__(self):
        return hash(self.fun)

    def __call__(self, *args, **kwargs):
        return self.fun(*args, **kwargs)

    def __add__(self, *args, **kwargs): name = "__add__"; return _rxsable(self, name, args, kwargs) # for +
    def __sub__(self, *args, **kwargs): name = "__sub__"; return _rxsable(self, name, args, kwargs) # for -
    def __mul__(self, *args, **kwargs): name = "__mul__"; return _rxsable(self, name, args, kwargs) # for *
    def __truediv__(self, *args, **kwargs): name = "__truediv__"; return _rxsable(self, name, args, kwargs) # for /
    def __floordiv__(self, *args, **kwargs): name = "__floordiv__"; return _rxsable(self, name, args, kwargs) # for //
    def __mod__(self, *args, **kwargs): name = "__mod__"; return _rxsable(self, name, args, kwargs) # for %
    def __pow__(self, *args, **kwargs): name = "__pow__"; return _rxsable(self, name, args, kwargs) # for **
    def __and__(self, *args, **kwargs): name = "__and__"; return _rxsable(self, name, args, kwargs) # for &
    def __xor__(self, *args, **kwargs): name = "__xor__"; return _rxsable(self, name, args, kwargs) # for ^
    def __or__(self, *args, **kwargs): name = "__or__"; return _rxsable(self, name, args, kwargs) # for |
    def __lshift__(self, *args, **kwargs): name = "__lshift__"; return _rxsable(self, name, args, kwargs) # for <<
    def __rshift__(self, *args, **kwargs): name = "__rshift__"; return _rxsable(self, name, args, kwargs) # for >>
    def __iadd__(self, *args, **kwargs): name = "__iadd__"; return _rxsable(self, name, args, kwargs) # for +=
    def __isub__(self, *args, **kwargs): name = "__isub__"; return _rxsable(self, name, args, kwargs) # for -=
    def __imul__(self, *args, **kwargs): name = "__imul__"; return _rxsable(self, name, args, kwargs) # for *=
    def __idiv__(self, *args, **kwargs): name = "__idiv__"; return _rxsable(self, name, args, kwargs) # for /=
    def __ifloordiv__(self, *args, **kwargs): name = "__ifloordiv__"; return _rxsable(self, name, args, kwargs) # for //=
    def __imod__(self, *args, **kwargs): name = "__imod__"; return _rxsable(self, name, args, kwargs) # for %=
    def __ipow__(self, *args, **kwargs): name = "__ipow__"; return _rxsable(self, name, args, kwargs) # for **=
    def __ilshift__(self, *args, **kwargs): name = "__ilshift__"; return _rxsable(self, name, args, kwargs) # for <<=
    def __irshift__(self, *args, **kwargs): name = "__irshift__"; return _rxsable(self, name, args, kwargs) # for >>=
    def __iand__(self, *args, **kwargs): name = "__iand__"; return _rxsable(self, name, args, kwargs) # for &=
    def __ixor__(self, *args, **kwargs): name = "__ixor__"; return _rxsable(self, name, args, kwargs) # for ^=
    def __ior__(self, *args, **kwargs): name = "__ior__"; return _rxsable(self, name, args, kwargs) # for |=
    def __neg__(self, *args, **kwargs): name = "__neg__"; return _rxsable(self, name, args, kwargs) # for –
    def __pos__(self, *args, **kwargs): name = "__pos__"; return _rxsable(self, name, args, kwargs) # for +
    def __abs__(self, *args, **kwargs): name = "__abs__"; return _rxsable(self, name, args, kwargs) # for abs()
    def __invert__(self, *args, **kwargs): name = "__invert__"; return _rxsable(self, name, args, kwargs) # for ~
    def __complex__(self, *args, **kwargs): name = "__complex__"; return _rxsable(self, name, args, kwargs) # for complex()
    def __int__(self, *args, **kwargs): name = "__int__"; return _rxsable(self, name, args, kwargs) # for int()
    def __long__(self, *args, **kwargs): name = "__long__"; return _rxsable(self, name, args, kwargs) # for long()
    def __float__(self, *args, **kwargs): name = "__float__"; return _rxsable(self, name, args, kwargs) # for float()
    def __oct__(self, *args, **kwargs): name = "__oct__"; return _rxsable(self, name, args, kwargs) # for oct()
    def __hex__(self, *args, **kwargs): name = "__hex__"; return _rxsable(self, name, args, kwargs) # for hex()
    def __lt__(self, *args, **kwargs): name = "__lt__"; return _rxsable(self, name, args, kwargs) # for <
    def __le__(self, *args, **kwargs): name = "__le__"; return _rxsable(self, name, args, kwargs) # for <=
    def __eq__(self, *args, **kwargs): name = "__eq__"; return _rxsable(self, name, args, kwargs) # for ==
    def __ne__(self, *args, **kwargs): name = "__ne__"; return _rxsable(self, name, args, kwargs) # for !=
    def __ge__(self, *args, **kwargs): name = "__ge__"; return _rxsable(self, name, args, kwargs) # for >=
    def __gt__(self, *args, **kwargs): name = "__gt__"; return _rxsable(self, name, args, kwargs) # for >
    def __matmul__(self, *args, **kwargs): name = "__matmul__"; return _rxsable(self, name, args, kwargs) # for >
    def __rmatmul__(self, *args, **kwargs): name = "__rmatmul__"; return _rxsable(self, name, args, kwargs) # for >


# @__add__
# @__sub__
# @__and__
@wushu('__add__')
@wushu('sub')
@wushu('and')
def f(item):

    if type(item) == int:
        print(item)
    else:
        print([*item])


if __name__ == "__main__":
    
    f (34)
    f+ 34
    f- 34
    f& 25
    f& range(10)
    # 34 -f