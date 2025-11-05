class employee:
    language = "Python"
    salary = 12000000000
    def getinfo(self):
        print(f"your language is {self.language} and your salary is {self.salary}") 

    @staticmethod  # marking with this keyword means this func doesn't need an argument

    def greet():
        print ("good morning")      

harry = employee()
harry.language = "Unity"
harry.greet()
harry.getinfo()           # this one and the lower one are same instruction
#employee.getinfo(harry)     