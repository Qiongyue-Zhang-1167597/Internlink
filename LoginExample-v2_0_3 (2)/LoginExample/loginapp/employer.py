from loginapp import app
from loginapp import db
from flask import redirect, render_template, session, url_for
from loginapp.utils import login_required, role_required

@app.route('/employer/home')
@login_required
@role_required('employer')
def employer_home():
    return render_template('employer_home.html')
