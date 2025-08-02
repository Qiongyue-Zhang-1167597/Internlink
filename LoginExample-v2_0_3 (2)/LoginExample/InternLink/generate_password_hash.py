from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
plain_password = input("Enter the password you want to hash: ")
hashed = bcrypt.generate_password_hash(plain_password).decode('utf-8')
print("Hashed password:")
print(hashed)
