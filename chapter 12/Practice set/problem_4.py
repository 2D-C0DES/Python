try:
    a = int(input("Enter the a : "))
    b = int(input("Enter the b : "))
    print(a/b)

except ZeroDivisionError as v:
    print(v)
    print("Infinite")


