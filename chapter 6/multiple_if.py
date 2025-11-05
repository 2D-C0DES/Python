# this is a program which checks if a person is eliible for drivin license

a = int(input("Enter your age : "))
# if statement No.1
if(a%2 == 0):
    print("your age is even ")

# if statement No.2

if(a>=18):
    print("You are eligible")

elif(a<=0):
    print("this is na invalid age")

else :
    print("You are not eliible")

print("End of program")