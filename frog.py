"""
Functional pROGramming paradigms.

I wanted to write some functional programming features.
One question remains though : should streams be immutable ?
Wouldn't that impact memory usage if so ? (does the interpreter
create a new copy of the stream everytime we do a new operation
on it ?)
For now, streams are mutable and work that way.
"""

def flatMap(func, data):
    result = []
    for i in data:
        res = func(i)
        # if type(res) in [list, tuple]:
        #     result += res
        # else:
        #     result.append(res)
        result += res
    return result

def reduce(func, data, ind=-1):
    result = []
    if not data:
        return result
    if ind < 0:
        result = data[0]
        for i in data[1:]:
            result = func(result, i)            
    
    return result

def combine(func, data, ind=2):
    return [func(data[i:i+ind]) for i in range(0, len(data), ind)]

def nmap(func, data, ind=2):
    return [func(*data[i:i+ind]) for i in range(0, len(data), ind)]

def accumulate(func, data, ind=2):
    result = []
    p = None
    for i in range(0, len(data), ind):
        a = func(*data[i:i+ind])
        if p:
            p = p + a
        else:
            p = a
        result.append(p)
    return result

def is_(x):
    return x

def select(func, data, ind):
    return [func(data[i:i+ind])[ind] for i in range(0, len(data), ind)]
    

def categorize(func, data):
    return data

def dmap(func, data):
    return list(map(func, data))

import operator as op

immutable_streams = False

def rimmutable(stream, data):
    if immutable_streams:
        return Stream(data)
    else:
        stream.data = data
        return stream

class CC:
    def __init__(self, stream, metafunc):
        print('target:', stream)
        self.stream, self.metafunc = stream, metafunc
        
    def __call__(self, func, *args, **kwargs):
        self.stream.data = self.metafunc(func, self.stream.data, *args, **kwargs)
        return self.stream

class Stream:
    def __init__(self, data):
        self.data = data
        
    def __getattr__(self, name):
        item = globals().get(name, None)
        if item:
            return CC(self, item)
        else:
            raise Exception('{} : No such function'.format(name))
            
    def filter(self, func):
        self.data = list(filter(func, self.data))
        return self
    
    def map(self, func):
        self.data = list(map(func, self.data))
        return self
    
    def reduce(self, func, ind=-1):
        self.data = reduce(func, self.data, ind)
        return self
    
    def __str__(self):
        return str(self.data)
    
    def __repr__(self):
        return self.__str__()
    
    def __iter__(self):
        return self.data.__iter__()
    
    def tolist(self):
        try:
            self.data = list(self.data)
        except TypeError as te:
            pass
        try:
            self.data = [self.data]
        except:
            pass
        return self
    
    def __getitem__(self, d):
        return Stream(self.data[d])

    def __setitem__(self, idx, value):
        self.data[idx] = value

    def __len__(self):
        return len(self.data)
    
    def fract(self, n):
        if n < 1 and n >= 0:
            return self[:int(n*len(self.data))]
        elif n > 0:
            return self[:n]
        
    def sample(self, n):
        return fract(n)
