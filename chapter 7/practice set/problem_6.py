prod = 1
n = int(input("enter the number you wannt the factorial : "))

i = 1

while(i<=n):
        prod *=i
        i+=1

print(f"the factorial of the numbers is : {prod}")