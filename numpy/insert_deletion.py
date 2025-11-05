import numpy as np

arr = np.array([78,45,12,63,85,69,15])
arr_new = np.insert(arr,4,90)

print(arr_new)
print()

arr_2 = np.array([[5,8,9],[8,3,41]])

arr_new1 = np.insert(arr_2,2,[63,93,30],axis=0)
arr_new2 = np.append(arr_2,[[63,93,30]],axis = 0)
print(arr_new1)
print()
print(arr_new2)
print()


arr_new3 = np.delete(arr_new2,2,axis =0)

print(arr_new3)
print()

arr_new4 = np.delete(arr,5)
print(arr_new4)