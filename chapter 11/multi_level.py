class employee:
    a = 1

class programmer(employee):
    b =2 

class managger(programmer):
    c = 4

e = employee()
print(e.a)
print(e.b)  #  this will be showing error because the b attribute is not present in the employee class

p = programmer()
print(p.a)
print(p.b)







