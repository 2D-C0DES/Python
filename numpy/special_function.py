import numpy as np

# shuffle
# unique
# resize
# flatten
# ravel

arr = np.array([1,34,56,78,23,7,45,23,89,56,45])

np.random.shuffle(arr)
print(arr)
print()
arr_new = np.unique(arr,return_index= True,return_counts=True)
print(arr_new)

arr_2 = np.array([[5,8,9,6],[8,3,41,69]])
arr_new1 = np.resize(arr_2,(4,2))
print()
print(arr_new1)

print()
print(arr_2.flatten(order = "F"))

