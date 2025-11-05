import numpy as np

# shape to know the shape of the array

# b = np.array([[45,27,38,64],[45,10,82,64]])
# print(b)
# print()
# print(b.ndim)
# print()
# print(b.shape)
# print()


# making a one dimensional array into multidimensional
# b = np.array([45,27,38,64] , ndmin = 5)
# print(b)
# print()
# print(b.shape)


# reshaping into diff types of multidimensional
b = np.array([45,27,38,64,23,56,85,75,42,36,78,30])
# c = b.reshape(2,6)
c = b.reshape(3,2,2)
print(c)
print()
print(c.ndim)
print()
print(c.shape)
print()


d = c.reshape(-1)  # -1 is used to reshaping the array into one dimensional
print(d)
print()
print(d.ndim)
print()
print(d.shape)
print()




