import math
# name = input("Enter your name: ")
# print(f"Name: {name}")
# 
# The input from the user is treated as a string. 
# Even if, in the example above, you can input a number, the Python interpreter will still treat it as a string.
# 
# number = input("Give your number to return square root from?: ")
# y = math.sqrt(float(number))
# print(f"You square root: {y}")
# 
y = True
while y == True:
    x = input("Enter a number:")
    try:
        x = float(x)
        y = False
    except:
        print("Wrong input, please try again.")
print("Thank you")
