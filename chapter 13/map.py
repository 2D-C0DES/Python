from functools import reduce

# map example

l = [1,2,3,4,5,]

square = lambda i : i**2

sq = map(square,l)
squared_list = list(sq)

print(squared_list)
# filter example

def even(n):
    if (n%2 == 0):
        return True
    else:
        return False    

OnlyEven =list(filter(even,l))

print(OnlyEven)


# # reduce examples

def sum(a,b):
    return a+b

mul = lambda x,y : x*y

print(reduce(mul,l))

print(reduce(sum,l))
