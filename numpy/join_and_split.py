import numpy as np

arr_1 = np.array([[4,7,8,9],[8,9,6,2]])
arr_2 = np.array([[5,8,9,6],[8,3,41,69]])

arr_3 = np.array([1,2,3,4,5,6,7,8])
arr_4 = np.array([1,2,3,4,5,6,7,8])


# arr_new = np.concatenate((arr_1,arr_2),axis = 1)  # this is concatenating the arrays according to axis
# print(arr_new)

arr_new1 = np.vstack((arr_1,arr_2))  # this prints equivalent to the axis = 0
arr_new2 = np.hstack((arr_1,arr_2))  # this prints equivalent to the axis = 1
print(arr_new1)
print()
print(arr_new2)

arr_new3 = np.array_split(arr_1,4,axis=1)
print()
print(arr_new3)