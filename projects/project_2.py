
from random import randint

computer_guess = randint(1, 101)
count = 0
while (True):
    my_guess = int(input("Enter your guess: "))
    
    count +=1
    if computer_guess > my_guess:
        print("Higher your guess.")   # as my guess is low it is needed to guess high
    elif computer_guess < my_guess:
        print("lower your guess.")    # as my guess is high it is needed too be low
    else:
        print(f"You have guessed it right in {count} times , it is {computer_guess}")
        break