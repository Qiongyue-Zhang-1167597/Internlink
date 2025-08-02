from InternLink import app
from InternLink import db
from flask import redirect, render_template, request, session, url_for
from flask_bcrypt import Bcrypt
import re
import string
import os
from werkzeug.utils import secure_filename
from InternLink import app 

# Create an instance of the Bcrypt class, which we'll be using to hash user
# passwords during login and registration.
flask_bcrypt = Bcrypt(app)

# Default role assigned to new users upon registration.
DEFAULT_USER_ROLE = 'student'

def user_home_url():
    """Generates a URL to the homepage for the currently logged-in user.
    
    If the user is not logged in, this returns the URL for the login page
    instead. If the user appears to be logged in, but the role stored in their
    session cookie is invalid (i.e. not a recognised role), it returns the URL
    for the logout page to clear that invalid session data."""
    if 'loggedin' in session:
        role = session.get('role', None)

        if role=='student':
            home_endpoint='student_home'
        elif role=='employer':
            home_endpoint='employer_home'
        elif role=='admin':
            home_endpoint='admin_home'
        else:
            home_endpoint = 'logout'
    else:
        home_endpoint = 'login'
    
    return url_for(home_endpoint)

@app.route('/')
def root():
    """Root endpoint (/)
    
    Methods:
    - get: Redirects guests to the login page, and redirects logged-in users to
        their own role-specific homepage.
    """
    return redirect(user_home_url())

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page endpoint.

    Methods:
    - get: Renders the login page.
    - post: Attempts to log the user in using the credentials supplied via the
        login form, and either:
        - Redirects the user to their role-specific homepage (if successful)
        - Renders the login page again with an error message (if unsuccessful).
    
    If the user is already logged in, both get and post requests will redirect
    to their role-specific homepage.
    """
    if 'loggedin' in session:
         return redirect(user_home_url())

    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        # Get the login details submitted by the user.
        username = request.form['username']
        password = request.form['password']

        # Attempt to validate the login details against the database.
        with db.get_cursor(dictionary=True) as cursor:
            # Try to retrieve the account details for the specified username.
            #
            # Note: we use a Python multiline string (triple quote) here to
            # make the query more readable in source code. This is just a style
            # choice: the line breaks are ignored by MySQL, and it would be
            # equally valid to put the whole SQL statement on one line like we
            # do at the beginning of the `signup` function.
            cursor.execute('''
                           SELECT user_id, username, password_hash, role
                           FROM user
                           WHERE username = %s;
                           ''', (username,))
            account = cursor.fetchone()
            
            if account is not None:
                # We found a matching account: now we need to check whether the
                # password they supplied matches the hash in our database.
                password_hash = account['password_hash']
                
                if flask_bcrypt.check_password_hash(password_hash, password):
                    # Password is correct. Save the user's ID, username, and role
                    # as session data, which we can access from other routes to
                    # determine who's currently logged in.
                    # 
                    # Users can potentially see and edit these details using their
                    # web browser. However, the session cookie is signed with our
                    # app's secret key. That means if they try to edit the cookie
                    # to impersonate another user, the signature will no longer
                    # match and Flask will know the session data is invalid.
                    session['loggedin'] = True
                    session['user_id'] = account['user_id']
                    session['username'] = account['username']
                    session['role'] = account['role']

                    if session['role'] == 'student':
                        return redirect(url_for('student_home'))
                    elif session['role'] == 'employer':
                        return redirect(url_for('employer_home'))
                    elif session['role'] == 'admin':
                        return redirect(url_for('admin_home'))
                    else:
                        return redirect(url_for('access_denied'))

                else:
                    return render_template('login.html',
                                           username=username,
                                           password_invalid=True)
            else:
                return render_template('login.html',
                                       username=username,
                                       username_invalid=True)

    return render_template('login.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if 'loggedin' in session:
         return redirect(user_home_url())
    
    if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'password' in request.form:
  
        if 'loggedin' in session:
         return redirect(user_home_url())
    
        if request.method == 'POST':
        
            print("--- Form Data Received ---")
            print(request.form)
        
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        full_name = request.form.get('full_name', '').strip()
        university = request.form.get('university', '').strip()
        course = request.form.get('course', '').strip()
        profile_image_file = request.files.get('profile_image')
        resume_pdf_file = request.files.get('resume_pdf')

        profile_image_filename = None
        resume_pdf_filename = None
        
        upload_folder = app.config.get('UPLOAD_FOLDER', os.path.join(app.root_path, 'static', 'uploads'))
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        if profile_image_file and profile_image_file.filename != '':
            profile_image_filename = secure_filename(profile_image_file.filename)
            profile_image_file.save(os.path.join(upload_folder, profile_image_filename))
            profile_image_filename = os.path.join('uploads', profile_image_filename).replace("\\", "/")

        if resume_pdf_file and resume_pdf_file.filename != '':
            resume_pdf_filename = secure_filename(resume_pdf_file.filename)
            resume_pdf_file.save(os.path.join(upload_folder, resume_pdf_filename))
            resume_pdf_filename = os.path.join('uploads', resume_pdf_filename).replace("\\", "/")

        username_error = None
        email_error = None
        password_error = None

        
        with db.get_cursor(dictionary=True) as cursor:
            cursor.execute('SELECT `user_id` FROM `user` WHERE `username` = %s;', (username,))
            if cursor.fetchone():
                username_error = 'An account already exists with this username.'
            
            cursor.execute('SELECT `user_id` FROM `user` WHERE `email` = %s;', (email,))
            if cursor.fetchone():
                email_error = 'An account already exists with this email address.'

        if not username_error:
            if len(username) > 50:
                username_error = 'Your username cannot exceed 50 characters.'
            elif not re.match(r'^[A-Za-z0-9_]+$', username):
                username_error = 'Your username can only contain letters, numbers, and underscores.'

        if not email_error:
            if len(email) > 100:
                email_error = 'Your email address cannot exceed 100 characters.'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                email_error = 'Invalid email address.'

        
        password_regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[' + re.escape(string.punctuation) + r']).{8,}$')
        
        
        confirm_password = request.form.get('confirm', '')

        
        if not password_regex.match(password):
            password_error = 'Password must be at least 8 characters long and contain uppercase, lowercase, a number, and a special character.'
        
        elif password != confirm_password:
            password_error = 'Passwords do not match.'

        if (username_error or email_error or password_error):
            return render_template('signup.html',
                                   username=username, email=email, full_name=full_name,
                                   university=university, course=course,
                                   username_error=username_error, email_error=email_error,
                                   password_error=password_error)

 
        password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')
        
        with db.get_cursor() as cursor:
            sql_user = """
                INSERT INTO `user` (`username`, `password_hash`, `email`, `role`, `status`, `full_name`, `profile_image`)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(sql_user, (username, password_hash, email, DEFAULT_USER_ROLE, 'active', full_name, profile_image_filename))
            
            new_user_id = cursor.lastrowid
            
            if new_user_id:
                sql_student = """
                    INSERT INTO `student` (`user_id`, `university`, `course`, `resume_path`)
                    VALUES (%s, %s, %s, %s);
                """
                cursor.execute(sql_student, (new_user_id, university, course, resume_pdf_filename))
            
            db.get_db().commit()
            
        return render_template('signup.html', signup_successful=True)

    return render_template('signup.html')


@app.route('/profile')
def profile():
    """User Profile page endpoint.

    Methods:
    - get: Renders the user profile page for the current user.

    If the user is not logged in, requests will redirect to the login page.
    """
    if 'loggedin' not in session:
         return redirect(url_for('login'))

    # Retrieve user profile from the database.
    with db.get_cursor(dictionary=True) as cursor:
        cursor.execute('SELECT username, email, role FROM user WHERE user_id = %s;',
                       (session['user_id'],))
        profile = cursor.fetchone()

    return render_template('profile.html', profile=profile)

@app.route('/logout')
def logout():
    """Logout endpoint.

    Methods:
    - get: Logs the current user out (if they were logged in to begin with),
        and redirects them to the login page.
    """
    # Note that nothing actually happens on the server when a user logs out: we
    # just remove the cookie from their web browser. They could technically log
    # back in by manually restoring the cookie we've just deleted. In a high-
    # security web app, you may need additional protections against this (e.g.
    # keeping a record of active sessions on the server side).
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('role', None)
    
    return redirect(url_for('login'))