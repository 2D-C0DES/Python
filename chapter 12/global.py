a = 634  # global variable by default

def func():
    global a # making global variable using the keywords
    a  = 89 
    print(a)  # local variable

print(a)
func()
print(a)
