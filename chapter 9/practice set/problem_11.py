with open("Poem.txt" , "r") as f:
    content = f.read()


with open("Python.txt" , "w") as f:
    f.write(content)    