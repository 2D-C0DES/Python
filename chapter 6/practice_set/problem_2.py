marks1 = int(input("Enter the marks :"))
marks2 = int(input("Enter the marks :"))
marks3 = int(input("Enter the marks :"))

# checkking for percentage

total_percentage = (marks1 + marks2 + marks3)/3

if (total_percentage >= 40 and marks1>=33 and marks2>=33 and marks3>= 33):
    print("You are passed")
else:
    print("You are fail")    