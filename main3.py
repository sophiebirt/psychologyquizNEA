from Classes.User import User

new_user = User.create_account("exampleUser", "examplePassword")
print("New user created:", new_user)



new_user = User.login("james", "james123") # This should return and error

new_user = User.login("exampleUser", "examplePassword")

print(new_user)