import random

def game():
    print("You are playing the game.")

    score =  random.randint(1,100)
    print(f"Your score is: {score} ")
    with open("Hi_score.txt" , "r") as f:
        hiscore = f.read()
        if(hiscore != ""):
            hiscore = int(hiscore)
        else:
            hiscore = 0


    if (score>hiscore):
        with open("Hi_score.txt", "w") as f :
            f.write(str(score))

    return score


game()
