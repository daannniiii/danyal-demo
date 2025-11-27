#5*****
#4*  *
#3* *
#2**
#1*
for i in range (5,0,-1):
    if i == 3 or i == 4 :
        print("*" + " "*(i-2) + "*")
    else :
        print(i*"*")