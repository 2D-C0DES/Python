class programmer:
    company = "Microsoft"

    def __init__(self , name , salary, pin) -> None:
        self.name = name 
        self.salary = salary
        self.pin = pin 


a = programmer("harry" , 1398976444,83426)
print (a.name,a.salary,a.pin)    
        