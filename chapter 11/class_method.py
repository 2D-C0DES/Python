class employee:
    a = 1


    @classmethod
    def show(cls):
        print (f"the class attribute is {cls.a}")


p = employee()
p.a =  54        
p.show()