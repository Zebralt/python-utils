CONTROL = '\033'
FORMAT =  CONTROL + '[%sm'
ENABLED = True 

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

def paint(*codes):
    return (FORMAT % ';'.join(map(str, codes))) * ENABLED

# should inherit from str
class Color:
    def __init__(self, *codes):
        self.codes = codes

    def __mod__(self, other):
        if type(other) == str:
            return paint(*self.codes) + other + FORMAT % CODES.RESET
        if type(other) == Color:
            return Color(*{*self.codes, *other.codes})
        return other

    def __add__(self, other):
        if type(other) == str:
            return str(self) + other
        if type(other) == Color:
            return Color(*{*self.codes, *other.codes})
        raise ValueError
    
    def __str__(self):
        return paint(*self.codes)

    def __repr__(self):
        return 'Color' + str(self.codes)

    def __call__(self, *args, godzilla=lambda x, *a, **k:print(x, *a, end='', **k), **kwargs):
        godzilla(str(self), *args, **kwargs)

class CODES:
    RESET = 0
    class FG:
        BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(90, 98)
        K, R, G, Y, B, M, C, W  = range(90, 98)

    class BG:
        BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(100, 108)
        K, R, G, Y, B, M, C, W  = range(100, 108)

class FG:
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = map(Color, range(90, 98))
    K, R, G, Y, B, M, C, W  = map(Color, range(90, 98))

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = map(Color, range(90, 98))
K, R, G, Y, B, M, C, W  = map(Color, range(90, 98))

BOLD = Color(1)

class BG:
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = map(Color, range(100, 108))
    K, R, G, Y, B, M, C, W  = map(Color, range(100, 108))

RESET = Color(CODES.RESET)


def make_hyperlink(title, url):
    HYPERLINK = '\033]8;;{url}\033\\{title}\033]8;;\033\\'
    return HYPERLINK.format(title=title, url=url)


# def cleanup_technicolor(python):
#     # look for import name
#     # remove all occurences
#     import re

#     lines = python.split('\n')

#     alias = None

#     for line in lines:

#         x = re.findall('import technicolor\s*$', line)
#         if x and alias is None:
#             alias = 'technicolor'

#         y = re.findall('import technicolor as (\w+)\s*$', line)
#         if y and alias is is None:
#             alias = y

        

    # return '\n'.join(lines)

if __name__ == '__main__':

    # print(color(FG.RED) % color(BG.G) % 'This is red %s' % 34, color(FG.BLUE) % 'then blue text')
    # print(RED % BG.K % 'This is red %s' % 34, BG.BLUE % CYAN % 'then blue text')
    # (GREEN % BG.K)('Hello')
    # RESET()

    # print(make_hyperlink('Click here!', 'https://google.com'))

    python = """
import technicolor as tech

print(tech.BLUE % 'This is text')
    """

    python = """
import technicolor

print(technicolor.BLUE % 'This is text')

    """

    # output = cleanup_technicolor(python)
    # open('readix.py', 'w+').write(output)