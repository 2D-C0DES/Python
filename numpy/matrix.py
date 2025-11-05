import numpy as np

# matrix functions

# transpose
# swapaxes
# inverse
# power
# determinate

x = np.matrix([[1,2,3],[4,5,6]])
y = np.matrix([[1,2],[3,4],[5,6]])
a = np.matrix([[1,2],[3,4]])

z = x * y # also can be written x.dot(y)

print(z)
print()
transpose = np.transpose(x)
print(transpose)
print()
swapped = np.swapaxes(y,0,1)
print(swapped)

inversed = np.linalg.inv(a)  # in this case input should be square matrix
print()
print(inversed)

print()
print(np.linalg.matrix_power(a,2))
print()
print(np.linalg.matrix_power(a,0))
print()
print(np.linalg.matrix_power(a,-2))
print()
d = np.linalg.det(a)
print(d)
