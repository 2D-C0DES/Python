a =(2,6,5,7,4,688,64,)

number = a.count(7)  # checks how many times the element is there

indx = a.index(688)   # it checks the index of the mentioned element

print (f"{number} and {indx}")

print (a*3)  # it's repeating the tuple *n times

print(96 in a)  # it checks the element is present or not in the tuple

print(a[:3])  # slicing

e, g, h = a[:3]   # shifting the mentioned tuple elements into different variables

print(e, g, h )