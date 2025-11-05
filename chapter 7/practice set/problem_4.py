n = int(input("enter the number : "))

count = 0

for i in range(2,n):
    if(n%i ==0):
        count+=1
        break
    

if(count==1  ):
    print("the entered number is composite")    
elif(n==2):
    print("the entered number is prime")
else:
    print("the entered number is prime")       
