try:
    a = int(input("Enter a number: "))
    print(a)

except Exception as e:
    print(e)    

else:
    print("I'm inside else cause the try block is run successfully")  