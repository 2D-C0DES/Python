def greatest(a,b,c):
    if(a>b and a>c):
        return a
    elif(b>c and b>a):
        return b
    elif(c>a and c>b):
        return c
    


a1 = int (input("enter the number : "))    
a2 = int (input("enter the number : "))    
a3 = int (input("enter the number : "))    
print(f"the greatest number is {greatest(a1,a2,a3)}")