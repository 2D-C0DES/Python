
f = open("Poem.txt", "r")

content = f.read()
print(content)

if("twinkle" in content):
    print("twinkle is present in the content")
else:
    print("twinkle is not present in the class")    


f.close()