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
        return round(self.num**(1/3))
    @staticmethod
    def hello():
        print("hello there")
    


a = calculator(64)
a.hello()
print(a.square())
print(a.cube())
print(a.square_root())
print(a.cube_root())






