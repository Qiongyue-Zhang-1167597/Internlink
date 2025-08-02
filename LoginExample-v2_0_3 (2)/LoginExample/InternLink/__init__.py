# This script runs automatically when our `InternLink` module is first loaded,
# and handles all the setup for our Flask app.
from flask import Flask
import os

app = Flask(__name__)

# Replace the default key for security
app.secret_key = 'KW9dfNV6qB7rWrY5J4aaxeuoqGUE6T532idUGQJaw2U' 

# File upload
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'png', 'jpg', 'jpeg'}

# Set upload directory path
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database connection
from InternLink import connect
from InternLink import db
db.init_db(app, connect.dbuser, connect.dbpass, connect.dbhost, connect.dbname,
           connect.dbport)

# Include all modules define Flask route-handling function
from InternLink import user
from InternLink import student
from InternLink import employer
from InternLink import admin