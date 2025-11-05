# with open("Python_checker.txt" , "w") as f:
#     f.write('''non-venomous reptile known for its impressive size and strength. 
# It constricts its prey, 
#The Python snake is a large,
# wrapping tightly around them to suffocate before consumption.''')


lineno = 1
with open("Python_checker.txt" , "r") as f :
    lines = f.readlines()

    for line in lines: 


     if ("Python" in line) :
        print(f"there is python in the content in line number {lineno}")
        break
     lineno +=1
    else:
       print("there is no python ")

