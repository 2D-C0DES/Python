class employee:
    language = "Python"
    salary = 12000000000    # this is a class attribute

debanjan = employee()
print(debanjan.language , debanjan.salary)  # this is a instance/object attribute

harry = employee()
harry.language = "Unity"   # while printing it first considers the instance attribute if not present
                           # then by default going to the class attribute
print(harry.language , harry.salary)