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

