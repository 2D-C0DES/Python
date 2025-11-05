class employee:

    @property
    def  name(self):
        return f"{self.fname} {self.lname}"
    
    @name.setter
    def name(self,value):
        self.fname = value.split(" ")[0]
        self.lname = value.split(" ")[1]


p = employee()
p.name = input("Enter your name : ")
print(f"Your name is {p.fname} {p.lname}")
        



    