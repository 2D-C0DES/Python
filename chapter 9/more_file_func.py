# To read lines in a file which has multiple lines , in this case we have the lines as a list in terminal

# f = open("myfile.txt")
# lines = f.readlines()  # this function helps to read the whole file at a once 
# print(lines , type(lines))
# f.close()

# to read the line of the file seperately

f = open("myFile.txt")
line =f.readline() # this func helps to read the line of the files seperately one by one 

while(line != ""):

    print(line)
    line = f.readline()   # in the loop this func can increment itself line by line by itself
    


f.close()
