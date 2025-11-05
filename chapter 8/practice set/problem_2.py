def C2F(c):
    return (9/5)*c +32


c = int(input("enter the celcius temperature : "))
d = round(C2F(c),2)    # round function basically rounds off the numbers 
print(f"the farenheit temperature is :{d}")