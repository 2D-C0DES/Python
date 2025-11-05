def addition(a : int , b : int) -> int:
    return f"The result of addition is {a + b}"


print(__name__)
if(__name__ == "__main__"):
    print ("This is the main module.")
    print(addition(8,9))
    print(__name__)
