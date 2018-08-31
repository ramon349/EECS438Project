from functools import singledispatch
from multimethod import multidispatch 

@multidispatch
def gen(x,y):
    if type(x).__name__ == type(y).__name__: 
        raise Exception(" Support for {thing} class is not implemented".format(thing=type(x).__name__))
    else: 
        raise Exception(" We don't suport using 2 different types")
    return 
@gen.register(str,str)
def _(y,x):
    return "We would do: {x} + {y}".format(x=x,y=y)
@gen.register(int,int)
def _(y,x):
    return x+y
@gen.register(float,float)
def _(y,x):
    return y +x
print('Using a string')
x =gen('hello','world')
print(x)
print('using an int')
x = gen(2,4)
print(x)
print(' Using an empty list')

try:
    x = gen([],{})
except Exception:
        print(' We found a bug heheh')
print(' Now trying with floats')
x = gen(2.0,4.0)
print(x)

def bad(x,y):
    return x +y
x = bad(1,2)
print(x)
def bad(x,y):
    return "lol jk"
x = bad(1,2)
print(x)



