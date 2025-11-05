class TwoDvector:
    def __init__(self , i,j) -> None:
        self.i = i
        self.j = j

    def show(self):
        print(f"the 2D vector is {self.i}i + {self.j}j")    


class ThreeDvector(TwoDvector):
    def __init__(self, i, j , k) -> None:
        super().__init__(i, j)
        self.k = k 

    def show(self):
        print(f"the 3D vector is {self.i}i + {self.j}j + {self.k}k")     



a = TwoDvector(1,3)
b = ThreeDvector(1,3,8)

a.show()
b.show()