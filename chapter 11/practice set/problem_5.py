class vector:
    def __init__(self,x,y,z) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __mul__(self,other):
        return (self.x * other.x  + self.y * other.y + self.z * other.z)

    def __add__(self,other):
        return vector(self.x+other.x , self.y + other.y,self.z + other.z)

    def __str__(self):
        return f"vector({self.x} , {self.y} , {self.z})"


a = vector(3,4,5)
b = vector(1,3,4)
c = vector(4,5,6)

print(a+b+c)
print(a*b)
print(b*c)

