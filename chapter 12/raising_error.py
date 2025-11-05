a = int(input("enter first number: "))
b = int(input("enter second number: "))

if(b==0):
    raise ZeroDivisionError("Our program is not meant to division by zero .")

else:
    print(f"The number a divided by b is {a / b}")