
import pydoc
import re


"""
A simple module to elegantly add color to text printed in terminal.
Using the mod operator, you can use easily insert it in your string format statements :

print(BLUE % 'This is a blue string !')

You can even chain them:

print(BLUE % BG.RED % 'This is a my name: %s' % name)

Using the mod operator will only color this one string. If you want to
dye the following text, just print the color by itself:

import technicolor as tech

print(tech.BLUE, end='')
# or
tech.BLUE() # Will call print(X, end='') by default
print('This is blue text')
print('This is still blue text')
print(tech.YELLOW + 'This is yellow text')
print('This is still yellow text', tech.RESET)
print('This is normal text')

"""

CONTROL = '\033'
FORMAT =  CONTROL + '[%sm'
ENABLED = True 
MODE = 'light'

# from functools import wraps
# def wrap_result(fun):
#     def decorator(xfun):
#         @wraps(xfun)
#         def wrapper(*args, **kwargs):
#             return fun(xfun(*args, **kwargs))
#         return wrapper
#     return decorator


# @wrap_result(ColoredText)
def paint(*codes):
    return (FORMAT % ';'.join(map(str, codes))) * ENABLED


class Brightness:
    def __get__(self, instance, owner):
        newcodes = [
            c + 60 if c in range(30, 50) else c
            for c in instance.codes            
        ]
        return Color(*newcodes)

class Darkness:
    def __get__(self, instance, owner):
        newcodes = [
            c - 60 if c in range(90, 110) else c
            for c in instance.codes            
        ]
        return Color(*newcodes)


class Color:

    dark = Darkness()
    light = Brightness()
    bright = light

    def __init__(self, *codes):
        self.codes = codes

    def __mod__(self, other):
        if type(other) == Color:
            return Color(*{*self.codes, *other.codes})
        else:
            return ColoredText(
                paint(*self.codes) + str(other) + FORMAT % CODES.RESET
            )
        return other

    def __matmul__(self, other):
        return self.__mod__(other)
    def __rmatmul__(self, other):
        return self.__mod__(other)

    def __add__(self, other):
        if type(other) == str:
            return str(self) + other
        if type(other) == Color:
            return Color(*{*self.codes, *other.codes})
        raise ValueError
    
    def __str__(self):
        return 'X1B' + str(self.codes)

    def __repr__(self):
        return 'Color' + str(self.codes)

    def __call__(self, *args, godzilla=lambda x, *a, **k:print(x, *a, end='', **k), **kwargs):
        godzilla(str(self), *args, **kwargs)


class CODES:
    RESET = 0
    class FG:
        # GRAY = 2
        BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(90, 98)
        K, R, G, Y, B, M, C, W  = range(90, 98)

    class BG:
        BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = MODE == 'light' and range(100, 108) or range(40, 48)
        K, R, G, Y, B, M, C, W  = range(100, 108)


# class FG:
#     # GRAY = Color(2)
#     BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = map(Color, MODE == 'light' and range(90, 98) or range(30, 38))
#     K, R, G, Y, B, M, C, W  = map(Color, range(90, 98))


class FG: pass
for name, value in vars(CODES.FG).items():
    if not re.match(r'^[A-Z]+$', name): continue
    setattr(FG, name, Color(value))

class BG: pass
for name, value in vars(CODES.BG).items():
    if not re.match(r'^[A-Z]+$', name): continue
    setattr(BG, name, Color(value))


# class BG:
#     BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = map(Color, range(100, 108))
#     K, R, G, Y, B, M, C, W  = map(Color, range(100, 108))

# GRAY = Color(2)
# BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = map(Color, MODE == 'light' and range(90, 98) or range(30, 38))
# K, R, G, Y, B, M, C, W  = map(Color, range(90, 98))

for name, value in vars(FG).items():
    globals()[name] = value

RESET = Color(CODES.RESET)
BOLD = BO = Color(1)
ITALIC = IT = Color(3)
UNDERLINE = UL = Color(4)
BLINK = BL = Color(5)
REVERSE = REV = Color(7)
# https://en.wikipedia.org/wiki/ANSI_escape_code
CONCEAL = Color(8)
DOUBLE_UNDERLINE = Color(21)
FRAME = Color(51)
ENCIRCLE = Color(52)
OVERLINE = Color(53)


RESET = Color(CODES.RESET)


def make_hyperlink(title, url):
    HYPERLINK = '\033]8;;{url}\033\\{title}\033]8;;\033\\'
    return HYPERLINK.format(title=title, url=url)

    # return '\n'.join(lines)



def demo():

    output = []

    to_show = {}

    for idx, (item, target) in enumerate(globals().items()):

        if item in ['CODES', 'CONTROL', 'FORMAT', 'ENABLED']:
            continue

        if not re.match('^[A-Z]+$', item):
            continue

        if type(target) != Color:
            continue

        if len(item) <= 3 and item not in ['RED']:
            continue

        to_show[item] = target

    for namespace in (FG, BG):
        for item, target in vars(namespace).items():
            if not re.match('^[A-Z]+$', item):
                continue
            if type(target) != Color:
                continue
            if len(item) <= 3 and item not in ['RED']:
                continue

            if namespace == BG:
                target = target % Color(30)

            item = namespace.__name__ + '.' + item
            to_show[item] = target
            
    line = ""

    for item, target in list(to_show.items()):

        if target.codes != target.dark.codes:
            to_show[item + '.dark'] = target.dark

        if target.codes != target.light.codes:
            to_show[item + '.light'] = target

    for idx, (item, target) in enumerate(sorted(to_show.items(), key=lambda x: x[0].count('.'))):
    

        """
        Coloring charaters throws off the formatting ...
        Maybe we could have ColoredText act like a str with a different __format__ / __str__ / __repr__ / __len__
        implementation that removes
        """

        line += '{:-4}:'.format(target.codes[0]) + '{:30}'.format(target % item)

        if not (idx - 2)%3:
            output += [line]
            line = ''

    output = '\n'.join(output) + '\n'
    output = UL % 'Demonstrating colors:\n\n '.title() + output
    pydoc.pipepager(output, cmd='less -R')
    # print(output)


import re

def strip_control_characters(text):
    return re.sub(r'\x1b\[[0-9;]+m', '', text)

def find_control_characters(text):
    return re.findall(r'\x1b\[[0-9;]+m', text)


class ColoredText(str):

    def __new__(cls, *a, **kw):
        return str.__new__(cls, *a, **kw)

    def __init__(self, _str, *a):
        self.inner = str(_str)

    def __format__(self, info):

        regex = r'(?<!\.)[0-9]+(?!f)'

        m = re.search(regex, info)
        if m:
        # find special chars
            specs = find_control_characters(self.inner)
        # Now, edit format if number in it:
            added_length = sum(map(len, specs))
            new_length = int(m.group()) + added_length
            a, b = m.span()
            info = ''.join((info[:a], str(new_length), info[b:]))

        return self.inner.__format__(info)


def test_colored_format():
    
    print('The following lines should have the same length on screen: ')
    
    print('   {:<30}'.format('this is'), '|')
    print('   {:<30}'.format(RED % 'this is'), '|')
    print('   {:<30}'.format(BG.RED % 'this is'), '|')

    assert ColoredText(RED % 'this is') == RED % 'this is'

    xt = ColoredText(RED % 'this is')
    print('xt', '{:<30}'.format(xt), '|')

    vt = ColoredText(RED % 'this ' + BLUE % 'i' + YELLOW % 's')
    print('vt', '{:<30}'.format(vt), '|')

    print('cb', '{:<30}'.format(Y % BG.K % REVERSE % 'this is'), '|')
    print('cb', '{:<30}'.format(Y % BG.K % 'this is'), '|')


if __name__ == '__main__':

    demo()
    # test_colored_format()

    print(make_hyperlink('Click here!', 'https://google.com'))
    # print(HYPERLINK('https://google.com') % 'Click here')
    # 'Click here' @link('google.com')
    
    print('text' @GREEN @BG.RED)
    print(CYAN@ 'text' @REVERSE)