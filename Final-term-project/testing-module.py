import json 
print("="*50)
print("WELLCOME TO CARNIVEL CORNER".center(50))
print("="*50,"\n LOGIN AS:\n 1.USER(U)\n 2.VENDER(V)\n 3.GUEST(G)\n 4.ADMIN(A)")
# get user type and verify
user_type = input()
if user_type == "u" or "U":
    print("user")
elif user_type == "v" or "V":
    print("vender")
    
elif user_type == "g" or "G":
    print("guest")
elif user_type == "a" or "A":
    print("Admin")
else:
    print("You entered an INVALID input")
