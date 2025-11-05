import numpy as np

# var = np.array([1,2,3,4])
# var_add = var +3
# print(var_add)


# var1 = np.array([1,2,3,4])
# var2 = np.array([5,6,7,8])

# var_add = var1 + var2

# print(var_add)
# print( np.multiply(var1,var2))  # also can be written as var1 * var2

# var1 = np.array([1,2,3,4])
# var2 = np.array([5,6,7,8])

# var_division = np.divide(var1,var2)
# print(var_division)



# like the previous operations also we can perform other arithmetic
# operation by using directly the sign or np.name_of_operation()

# operations on 2D arrays

var_21 = np.array([[12,23,34,45] , [78,25,63,59]])
var_22 = np.array([[67,78,90,60] , [89,57,56,26]])
var1 = np.array([0,22/42,22/28,22/21,22/14])

print(var_21 + var_22)
print(np.add(var_21,var_22))

print(np.reciprocal(var_21))

# it is easy in an one dimensional array to know the max and min element

print(np.min(var_21,axis = 1 )) # it is specially for the 2D arrays
print()
print(np.min(var1) , np.argmin(var1))
print(np.max(var1) , np.argmax(var1))
# here argmin and argmax function helps to find the position of the element

# tan theta

var_sin= np.sin(var1)
var_cos = np.cos(var1)
var_tan = var_sin/var_cos

var2 = np.array([5,6,7,8])

print(var_sin)
print(var_cos)
print(var_tan)

print(np.cumsum(var2))

