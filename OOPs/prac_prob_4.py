class Employee:
    def __init__(self,role,dept,salary):
        self.role = role
        self.dept = dept
        self.salary = salary

    def ShowDetails(self):
        print(f"Role = {self.role} , Department = {self.dept} , Salary = {self.salary}")
        
class engineer(Employee):
    def __init__(self,age ,name ):
        self.age =  age 
        self.name = name
        super().__init__("Engineer", "IT", 78534,)

    

# e1 = Employee("Senior Manager" , "Cyber Security" , 234909)
# e1.ShowDetails()

eng1 = engineer(20,"Debanjan")
eng1.ShowDetails()