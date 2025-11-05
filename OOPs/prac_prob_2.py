class Account:
    def __init__(self,balance,acc_no):
        self.balance = balance
        self.account_no = acc_no


    def debit(self,amount):
        self.balance -= amount
        print(f"{amount} amount was debited and the total balance is {self.get_balance()}")  


    def credit(self,amount):
        self.balance += amount
        print(f"{amount} amount was credited and the total balance is {self.get_balance()}") 

 
    def get_balance(self):
        return self.balance
    


acc1 = Account(6532 , "0445010264518")
acc1.debit(1894)
acc1.credit(2000)
