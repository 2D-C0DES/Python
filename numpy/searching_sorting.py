import numpy as np

x = np.array([1,2,3,4,34,52,89])

y = np.where((x%2) == 0)

print(y)   # y is the collection of all the index 

z = np.searchsorted(x,[45,78,83])
print(z)


arr = np.array([1,45,56,89,34,72,69,23])
print(np.sort(arr))