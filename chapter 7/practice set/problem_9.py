n = int(input("enter the number : "))

for i in range(1,n+1):
    if(i==n or i==1):
        print("*"*n)
    else:
        print("*",end="")
        print(" "*(n-2),end ="")
        print("*")
print("")