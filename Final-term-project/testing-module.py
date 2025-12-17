import json 
print("="*50)
print("WELLCOME TO CARNIVEL CORNER".center(50))
print("="*50,"\n LOGIN AS:\n 1.USER(U)\n 2.VENDER(V)\n 3.GUEST(G)\n 4.ADMIN(A)")
# get user type and verify
user_type = input()
user_type = user_type.lower()

if user_type == "u":
    print("user")
elif user_type == "v":
    print("vender")
elif user_type == "g":
    print("guest")
elif user_type == "a":
    print("Admin")
else:
    print("You entered an INVALID input")
