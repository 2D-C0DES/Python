import numpy as np
# d.type is used to check the data type in numpy
#  astype() is a function used to convert the datatypes




b = np.array([45,27,38,64])
print(b)
print("Data type: ",b.dtype)

# data type conversion
# b1 = np.array([45,27,38,64],dtype =  float)
# print(b1)
# print("Data type: ",b1.dtype)

# b2 = np.str_(b1)
# print(b2)
# print("Data type : ",b2.dtype)
#

# astype() function

b2 = b.astype(str)
print(b2)
print("Data type : ",b2.dtype)