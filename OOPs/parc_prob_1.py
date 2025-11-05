class student:
    def __init__(self,name,marks):
        self.name = name 
        self.marks = marks

    def avg(self):
        sum = 0
        for mark in self.marks:
            sum += mark

        print(f"Hiii...{self.name} your average marks is {sum/3}")    
                    


s1 = student("Debanjan", [89,83,92])
s1.avg()                    