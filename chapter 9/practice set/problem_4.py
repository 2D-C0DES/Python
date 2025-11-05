
# f = open("Mything.txt" , "w")


# f.write("donkey is not a bad word although it is a nice word")

# f.close() 

with open("Mything.txt" , "r") as f:
    cont = f.read()
    contNew = cont.replace("donkey" , "#####")

with open("Mything.txt" , "w") as f:
    f.write(contNew)    