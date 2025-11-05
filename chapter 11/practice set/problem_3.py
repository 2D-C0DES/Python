
class employee:
    def __init__(self, salary, increment) -> None:
        self.salary = salary
        self.increment = increment

    @property
    def salaryafterincrement(self):
        return (self.salary + self.salary * (self.increment/100))

    @salaryafterincrement.setter
    def salaryafterincrement(self, salary):
        self.increment = ((salary / self.salary) - 1) * 100

a = employee(2400, 20)

print(a.salaryafterincrement)
a.salaryafterincrement = 4560

print(round(a.increment))


