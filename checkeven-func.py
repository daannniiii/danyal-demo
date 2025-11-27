def noteven (a):
    if a % 2 == 0 :
        return 1 
    else:
        return 0
def tilleven (b):
    for i in range(2,b+1,2):
        print(i)
n = int (input("Enter a number:"))
if noteven(n):
    print("The number is even")
    tilleven(n)
else:
    print("The number entered is odd")