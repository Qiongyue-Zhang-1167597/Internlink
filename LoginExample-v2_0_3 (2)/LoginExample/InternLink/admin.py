from InternLink import app
from InternLink import db
from flask import redirect, render_template, session, url_for
from InternLink.utils import login_required, role_required


@app.route('/admin/home')
@login_required
@role_required('admin')
def admin_home():
    cursor = db.get_db().cursor(dictionary=True)
    username = session['username']
    cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()

    return render_template('admin_home.html', user=user)