

class Number:
    def __init__(self, n):
        self.n = n

    def __add__(self, num):
        return Number(self.n + num.n)
    
    def __str__(self , num) -> str:
        return f"{self.n + num}"

p = Number(2)
q = Number(3)

print ((p + q).n)



