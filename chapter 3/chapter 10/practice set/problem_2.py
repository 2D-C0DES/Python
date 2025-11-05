class calculator:

    def __init__(self , num) -> None:
        self.num = num 

    def square(self):
        return self.num**2
    def cube(self):
        return self.num **3
    def square_root(self):
        return self.num**(1/2)
    def cube_root(self):
        return (self.num**(1/3))
    

n = int(input("enter the number:"))
a = calculator(n)
print(a.square())
print(a.cube())
print(a.square_root())
print(a.cube_root())






