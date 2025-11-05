
def rem(l,word):

    n = []
    for item in l :
        if not(item == word):
            n.append(item.strip(word))
        return n
    



l = ["Harry","Rohan","Debanjan", "an"]
b = input("enter the word you want to strip : ")
print(rem(l,b))