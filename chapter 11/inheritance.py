class employee:
    company = "IBM"

    def __init__(self,name,salary,language) -> None:
        self.name = name
        self.salary = salary
        self.language = language
    def show(self):
        print(f"the name of the employee is {self.name} and salary is {self.salary} ")


# class programmer:
#     company = "IBM Inffotech"
#     def __init__(self,name,salary,language ) -> None:
#         self.name = name
#         self.salary = salary
#         self.language = language
#     def show(self):
#         print(f"the name of the employee is {self.name} and salary is {self.salary}.He is  expert at {self.salary } language ")


class programmer(employee):
    company = "IBM Infotech"
    def show(self):
        print(f"the name of the employee is {self.name} and salary is {self.salary}.He is expert at {self.language } language ")

a = employee("harry",862628,"Solidity")
b = programmer("Debanjan" , 96527200, "unity")

a.show()
b.show()
    