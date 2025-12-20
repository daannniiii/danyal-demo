import json 
def welcome ():
    print("="*50)    
    print("WELLCOME TO CARNIVEL CORNER".center(50))
    print("="*50)
def login_info():
    print("LOGIN AS:\n 1.USER(U)\n 2.VENDER(V)\n 3.GUEST(G)\n 4.ADMIN(A)".center(50))
    # get user type and verify
    user_type = input()
    user_type = user_type.lower()
    return user_type 
def u_type(user_type):
    
welcome()
if user_type == "u":
        print("user")
    elif user_type == "v":
        print("vendor")
    elif user_type == "g":
        print("guest")
    elif user_type == "a":
        print("Admin")
    else:
        print("You entered an Invalid input:")