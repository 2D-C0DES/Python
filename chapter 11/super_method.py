class employee:
    def __init__(self) -> None:
        print("constrtuctor of employee")
    

    a =1 
class programmer(employee):
        def __init__(self) -> None:
            print("constrtuctor of programmer")


        b =2 

class manager(programmer):
        
        def __init__(self) -> None:
            super().__init__()   # here we use the super method to use the method of parent classes

            print("constrtuctor of manager")

        
        c = 4

# e = employee()
# print(e.a)
# print(e.b)  #  this will be showing error because the b attribute is not present in the employee class

p = manager()
print(p.a)
print(p.b)







