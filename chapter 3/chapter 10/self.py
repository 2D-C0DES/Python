class employee:
    language = "Python"
    salary = 12000000000
    def getinfo(self):
        print(f"your language is {self.language} and your salary is {self.salary}")    # this is a class attribute
    
# debanjan = employee()
# print(debanjan.language , debanjan.salary)  # this is a instance/object attribute

harry = employee()
harry.language = "Unity"
harry.getinfo()           # this one and the lower one are same instruction
employee.getinfo(harry)     

# while printing it first considers the instance attribute if not present
# then by default going to the class attribute
#print(harry.language , harry.salary)