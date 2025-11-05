import numpy as np
# list of used functions

# 1. np.zeros()  for  creating zero arrays
# 2. np.ones()  for creating one arrays
# 3. np.empty()  for creating empty arrays
# 4. np.arange() for creating range arrays 
# 5. np.eye() for creating arrays with diagoanl elements 1
# 6. np.linspace() for creating arrays with elements spaced by a specefic interval


# zero arrays
arr_zero = np.zeros(4)

arr_zero1 = np.zeros((4,5))
print(arr_zero)
print("\n")
print(arr_zero1)
print("\n")

# ones arrays 

arr_one=np.ones(4)
arr_one2 = np.ones((1,2,3))

print(arr_one)
print("\n")
print(arr_one2)
print("\n")

# empty arrays

# arr_emp = np.empty(3)
# arr_emp1= np.empty((2,3))

# print(arr_emp)
# print("\n")
# print(arr_emp1)
# print("\n")

# Range arrays

arr_rng = np.arange(56)

# print(arr_rng)

# diagonal elemnets with 1
arr_dia = np.eye(2,3)

print(arr_dia)
print("\n")  

# array with specefic interval

arr_interval = np.linspace(1,20,num = 5 )

print(arr_interval)