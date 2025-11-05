import numpy as np


arr_1 = np.array([1,2,3,4,5,6,7,8])
arr_2 = np.array([[1,2,3,4] , [5,6,7,8]])
arr_3 = np.array([[[1,2,3],[4,5,6]],[[7,8,9],[10,11,12]]])

print(arr_1)
print(arr_2)
print(arr_3)

print(arr_1[2])
print(arr_2[0,1])
print(arr_3[0,1,2])

print(arr_1[1:4:2]) # this is 1D array slicing arr[start:stop:step]
print(arr_1[1:])
print(arr_1[:5])


# 2D array slicing

print(arr_2[0,1:])
print(arr_3[0,1,1:])