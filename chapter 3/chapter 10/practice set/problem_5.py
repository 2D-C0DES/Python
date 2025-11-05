from random import randint


class train:




    def __init__(self , train_no):
        self.train_no = train_no


    def book(self,fro,to):
        print(f"Ticket is booked in train no. {self.train_no} from {fro} to {to}")    
    def getStatus(self):
        print(f"Train number {self.train_no} is running on time")
    def getFare(self,fro,to):
        print(f"Ticket fare in train number {self.train_no} from {fro} to {to} is {randint(22,5362)}")        



a = train(312456)

a.book("Belgharia" , "Kalyani")
a.getStatus()
a.getFare("Belgharia" , "kalyani")

