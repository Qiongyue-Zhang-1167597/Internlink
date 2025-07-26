from loginapp import app
from loginapp import db
from flask import redirect, render_template, session, url_for
from loginapp.utils import login_required, role_required 

@app.route('/student/home')
@login_required
@role_required('student')
def student_home():
    """student Homepage endpoint.

    Methods:
    - get: Renders the homepage for the current student.

    If the user is not logged in or has wrong role, decorators will handle redirection.
    """
    return render_template('student_home.html')