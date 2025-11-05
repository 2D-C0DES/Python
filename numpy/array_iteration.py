import numpy as np

arr_1 = np.array([1,2,3,4,5,6,7,8])

# for i in arr_1:
#     print(i)

arr_2 = np.array([[1,2,3,4] , [5,6,7,8]])

# for i in arr_2:
#     for j in i:
#         print(j)


# for  i in np.nditer(arr_2):  ## iterate without any for loop
#     print(i)

arr_3 = np.array([[[1,2,3],[4,5,6]],[[7,8,9],[10,11,12]]])

for i,d in np.ndenumerate(arr_3):  # prints with index
    print(i,d)