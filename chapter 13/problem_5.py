from functools import reduce
a = [2992,3920,9330,6746,626746]

def greater(a,b):
    if(a>b):
        return a 
    return b

print(reduce(greater,a))