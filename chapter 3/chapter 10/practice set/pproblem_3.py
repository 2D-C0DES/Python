class demo:
    a = 0



o = demo()
print(o.a)   # prints class atribute cuz no instance atribute is present
o.a = 4
print(o.a) # print something else because instance atribute is set    
print(demo.a)  # prints class attribute cuz class atribute doesn't change