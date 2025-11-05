class circle:
    def __init__(self , rad):
        self.rad = rad

    def area(self):
        area = (22*(self.rad**2))/7
        return area
    def perimeter(self):
        perimeter = (44*self.rad)/7
        return perimeter
    

C1 = circle(21)
print(C1.area())
print(C1.perimeter())

        