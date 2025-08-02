from InternLink import app
from InternLink import db
from flask import redirect, render_template, session, url_for, request
from InternLink.utils import login_required, role_required 

@app.route('/student/home')
@login_required
@role_required('student')
def student_home():
    """
    student Homepage endpoint.
    """
    cursor = db.get_db().cursor(dictionary=True)
    username = session['username']
    cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()

    return render_template('student_home.html', user=user)

@app.route('/student/internships')
@login_required
@role_required('student')
def browse_internships():
    """
    Browse internships with optional filters
    """
    cursor = db.get_db().cursor(dictionary=True)
    location = request.args.get('location')
    duration = request.args.get('duration')

    query = "SELECT * FROM internships WHERE 1=1"
    params = []

    if location:
        query += " AND location = %s"
        params.append(location)
    if duration:
        query += " AND duration = %s"
        params.append(duration)

    cursor.execute(query, params)
    internships = cursor.fetchall()
    cursor.close()

    return render_template('browse_internships.html', internships=internships)