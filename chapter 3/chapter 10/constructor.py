class employee:

    def __init__(self , name , salary , language):
        self.name = name 
        self.salary = salary
        self.language = language 
        print("I'm crreating an object.")     


    def getinfo(self):
        print(f"{self.name} your language is {self.language} and your salary is {self.salary}")

    

    @staticmethod  # marking with this keyword means this func doesn't need an argument
    def greet():
        print ("good morning")      

harry = employee("Harry" , 130000000 , "solidity")
harry.greet()
harry.getinfo()           # this one and the lower one are same instruction
#employee.getinfo(harry)     



