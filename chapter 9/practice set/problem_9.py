
f = open("Mything.txt" , "r")
content1 = f.read()

f.close()

with open("Python_checker.txt" , "r") as f:
    content2 = f.read()


if (content1 == content2):
    print("both the the files are having same content")
else:
    print("they are having different content")        