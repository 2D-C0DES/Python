class employee:
    company = "IBM"

    def __init__(self,name,salary,language) -> None:
        self.name = name
        self.salary = salary
        self.language = language
    def show(self):
        print(f"the name of the employee is {self.name} and company is {self.company} ")

class coder:
    language = "Python"

    def printlanguage(self):
        print(f"Out of the languages here is your language {self.language}")


class programmer(employee ,coder):
    company = "IBM Infotech"
    def showlanguage(self):
        print(f"the name of the employee is {self.name} and salary is {self.salary}.He is expert at {self.language} language ")

a = employee("harry",862628,"Solidity")
b = programmer("Debanjan" , 96527200, "unity")

b.showlanguage()
b.printlanguage()
    