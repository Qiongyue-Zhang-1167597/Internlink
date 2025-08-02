from collections import namedtuple
from flask import Flask
from flask_bcrypt import Bcrypt

UserAccount = namedtuple('UserAccount', ['username', 'password'])

# Initialize Flask and Bcrypt
app = Flask(__name__)
flask_bcrypt = Bcrypt(app)

users_to_create = [
    # --- Admins ---
    UserAccount('admin_linda', 'AdminPass123!'),
    UserAccount('admin_david', 'AdminSecure456$'),
    
    # --- Employers ---
    UserAccount('techcorp', 'TechCorpP@ss'),
    UserAccount('innovate_inc', 'InnovateP@ss'),
    UserAccount('datadigits', 'DataDigitsP@ss'),
    UserAccount('healthwell', 'HealthWellP@ss'),
    UserAccount('greenleaf', 'GreenLeafP@ss'),
    
    # --- Students ---
    UserAccount('janesmith', 'StudentPass1'),
    UserAccount('johndoe', '-'),
    UserAccount('emilyjones', 'StudentPass3'),
    UserAccount('michaelw', 'StudentPass4'),
    UserAccount('sarahb', 'StudentPass5'),
    UserAccount('kevin_davis', 'StudentPass6'),
    UserAccount('chloeg', 'StudentPass7'),
    UserAccount('jamesr', 'StudentPass8'),
    UserAccount('olivia_m', 'StudentPass9'),
    UserAccount('liam_h', 'StudentPass10'),
    UserAccount('ava_lopez', 'StudentPass11'),
    UserAccount('noah_gonzalez', 'StudentPass12'),
    UserAccount('isabella_p', 'StudentPass13'),
    UserAccount('ethan_sanchez', 'StudentPass14'),
    UserAccount('sophia_rivera', 'StudentPass15'),
    UserAccount('mason_t', 'StudentPass16'),
    UserAccount('mia_ramirez', 'StudentPass17'),
    UserAccount('jacob_f', 'StudentPass18'),
    UserAccount('charlotte_g', 'StudentPass19'),
    UserAccount('daniel_kim', 'StudentPass20')
]

# --- Main Script Logic ---
if __name__ == "__main__":
    print("\n--- Generating Password Hashes for Initial Users ---\n")
    print(f"{'Username':<20} | {'Password':<20} | {'Generated Hash (for SQL script)':<65}")
    print("-" * 115)

    for user in users_to_create:
       
        password_hash = flask_bcrypt.generate_password_hash(user.password).decode('utf-8')

        print(f"{user.username:<20} | {user.password:<20} | {password_hash:<65}")

    print("-" * 115)
    print("\nGeneration complete. Copy the hashes from the table above and paste them into your 'populate_database.sql' file.\n")



    










