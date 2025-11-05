words = [ "donkey", "gandu", "bal"]

with open("Mything.txt" , "r") as f :
    content = f.read()

for word in words:
    content = content.replace(word , "*" * len(word))

with open("Mything.txt" , "w") as f :
    f.write(content)        