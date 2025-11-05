class complex:
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y

    def __add__(self, c2):
        return complex(self.x + c2.x , self.y + c2.y)
    
    def __mul__(self,c2):
        real_part = self.x * c2.x - self.y * c2.y
        imaginary_part = self.x * c2.y + self.y *c2.x
        return complex(real_part , imaginary_part)
    
    def __str__(self) :
        return f"{self.x} + {self.y}i"
    


c1 = complex(1,2)
c2 = complex(3,4)

print(c1 + c2)
print(c1 * c2)