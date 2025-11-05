def divisible5(n):
    if (n%5==0):
        return True
    
    else:
        return False
    
a = [2992,3920,9330,6746,626746]

s = list(filter(divisible5,a))

print(s)