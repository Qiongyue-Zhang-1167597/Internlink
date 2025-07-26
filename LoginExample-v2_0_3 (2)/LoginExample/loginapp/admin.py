from loginapp import app
from loginapp import db
from flask import redirect, render_template, session, url_for
from loginapp.utils import login_required, role_required


@app.route('/admin/home')
@login_required
@role_required('admin')
def admin_home():
     
     return render_template('admin_home.html')