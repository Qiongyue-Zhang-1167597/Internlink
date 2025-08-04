
import os
from flask import Flask
from flask_bcrypt import Bcrypt

from . import user, student, admin, employer, db, connect 


app = Flask(__name__)


app.secret_key = 'KW9dfNV6qB7rWrY5J4aaxeuoqGUE6T532idUGQJaw2U'
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


user.flask_bcrypt.init_app(app)


db.init_db(app, connect.dbuser, connect.dbpass, connect.dbhost, connect.dbname, connect.dbport)


app.register_blueprint(user.user_bp)
app.register_blueprint(student.student_bp)
app.register_blueprint(admin.admin_bp)
app.register_blueprint(employer.employer_bp) 