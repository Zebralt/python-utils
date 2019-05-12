
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

# should inherit from str
class Color:
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
        GRAY = 2
        BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(90, 98)
        K, R, G, Y, B, M, C, W  = range(90, 98)

    class BG:
        BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(100, 108)
        K, R, G, Y, B, M, C, W  = range(100, 108)


class FG:
    GRAY = Color(2)
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = map(Color, range(90, 98))
    K, R, G, Y, B, M, C, W  = map(Color, range(90, 98))

GRAY = Color(2)
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = map(Color, range(90, 98))
K, R, G, Y, B, M, C, W  = map(Color, range(90, 98))

BOLD = BO = Color(1)
ITALIC = IT = Color(3)
UNDERLINE = UL = Color(4)
BLINK = BL = Color(5)
REVERSE = REV = Color(7)

class BG:
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = map(Color, range(100, 108))
    K, R, G, Y, B, M, C, W  = map(Color, range(100, 108))

RESET = Color(CODES.RESET)


def make_hyperlink(title, url):
    HYPERLINK = '\033]8;;{url}\033\\{title}\033]8;;\033\\'
    return HYPERLINK.format(title=title, url=url)

    # return '\n'.join(lines)


def demo():
    import re

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

            item = namespace.__name__ + '.' + item
            to_show[item] = target
            
    line = ""

    for idx, (item, target) in enumerate(to_show.items()):
    

        """
        Coloring charaters throws off the formatting ...
        Maybe we could have ColoredText act like a str with a different __format__ / __str__ / __repr__ / __len__
        implementation that removes
        """

        line += '{:30}'.format(target % item)

        if not (idx - 1)%3:
            print(line)
            line = ''

    print()



import re

def strip_control_characters(text):
    return re.sub(r'\x1b\[[0-9]+m', '', text)

def find_control_characters(text):
    return re.findall(r'\x1b\[[0-9]+m', text)


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

    # def __str__(self):
    #     return self.inner

    # def __repr__(self):
    #     return repr(self.inner)

    # def __add__(self, other):
    #     if type(other) == ColoredText:
    #         print('hey!')
    #     return self.inner + other

    # def __eq__(self, other):
    #     print('S', self.inner, type(self))
    #     print('O', other.inner, type(other))
    #     return self.inner == other.inner


if __name__ == '__main__':

    print('The following lines should have the same length on screen: ')
    
    print('   {:<30}'.format('this is'), '|')
    print('   {:<30}'.format(RED % 'this is'), '|')
    print('   {:<30}'.format(BG.RED % 'this is'), '|')

    # ct = ColoredText('this is', color=RED)
    # print('ct', '{:<30}'.format(ct), '|')

    assert ColoredText(RED % 'this is') == RED % 'this is'

    xt = ColoredText(RED % 'this is')
    print('xt', '{:<30}'.format(xt), '|')

    # print('---' * 30)

    vt = ColoredText(RED % 'this ' + BLUE % 'i' + YELLOW % 's')
    print('vt', '{:<30}'.format(vt), '|')


    demo()
    

    # print(make_hyperlink('Click here!', 'https://google.com'))
