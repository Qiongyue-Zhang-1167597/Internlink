from flask import Flask

from collections import namedtuple
from flask_bcrypt import Bcrypt

# Note: This script is intended to be run from the command line. It does not
# require a running Flask app, but it does need Flask-Bcrypt to be installed
# in your virtual environment.
flask_bcrypt = Bcrypt()

UserAccount = namedtuple('UserAccount', ['username', 'password'])

# --- Define all user accounts here ---
users_to_create = [
    # --- Admins ---
    UserAccount('admin_linda', 'AdminPass123!'),
    UserAccount('admin_david', 'AdminSecure456$'),

    # --- Employers ---
    UserAccount('techcorp',      'TechCorp@ss'),
    UserAccount('innovate_inc',  'InnovateP@ss'),
    UserAccount('datadigits',    'DataDigitsP@ss'),
    UserAccount('healthwell',    'HealthWellP@ss'),
    UserAccount('greenleaf',     'GreenLeafP@ss'),

    # --- Students (with new strong passwords) ---
    UserAccount('janesmith',   'BlueJay@2024'),
    UserAccount('johndoe',     'Starlight#789'),
    UserAccount('emilyjones',  'QuantumLeap!23'),
    UserAccount('michaelw',    'MidnightSun$55'),
    UserAccount('sarahb',      'Forest_Whisper1'),
    UserAccount('kevin_davis', 'CyberDragon%2'),
    UserAccount('chloeg',      'GalaxyQuest!77'),
    UserAccount('jamesr',      'PhoenixRise#8'),
    UserAccount('sophiam',     'CrimsonTide@90'),
    UserAccount('liam_h',      'SilverArrow_10'),
    UserAccount('ava_lopez',   'GoldenKey!112'),
    UserAccount('noah_gonzalez','VelvetNight$3'),
    UserAccount('isabella_p',  'EmeraldCity#45'),
    UserAccount('ethan_sanchez','SolarFlare@67'),
    UserAccount('sophia_rivera','Triton_Force8'),
    UserAccount('mason_t',     'WinterWolf!99'),
    UserAccount('mia_ramirez', 'OrionBelt$21'),
    UserAccount('jacob_f',     'NebulaDream#34'),
    UserAccount('charlotte_g', 'CometTrail@56'),
    UserAccount('daniel_kim',  'ApexPredator_7'),
]

print("-- SQL UPDATE statements for user passwords --")
print("-- Copy and paste these into your MySQL client --\n")

for user in users_to_create:
    password_hash = flask_bcrypt.generate_password_hash(user.password).decode('utf-8')
    
    # 生成 UPDATE 语句
    sql_statement = f"UPDATE user SET password_hash = '{password_hash}' WHERE username = '{user.username}';"
    
    print(sql_statement)


    










