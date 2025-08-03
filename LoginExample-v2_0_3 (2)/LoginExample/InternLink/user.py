import os
import re
import string


from flask import Blueprint, redirect, render_template, request, session, url_for, flash, current_app
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename


from .db import get_db
from .utils import login_required, role_required, is_password_strong


flask_bcrypt = Bcrypt()


user_bp = Blueprint('user', __name__)


DEFAULT_USER_ROLE = 'student'

def user_home_url():
    """Generates a URL to the homepage for the currently logged-in user."""
    if 'loggedin' in session:
        role = session.get('role', None)
        
        if role=='student':
            home_endpoint='student.student_home'
        elif role=='employer':
            home_endpoint='employer.employer_home'
        elif role=='admin':
            home_endpoint='admin.admin_home'
        else:
            home_endpoint = 'user.logout'
    else:
        home_endpoint = 'user.login'
    
    return url_for(home_endpoint)

@user_bp.route('/')
def root():
    """Root endpoint (/)"""
    return redirect(user_home_url())

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page endpoint."""
    if 'loggedin' in session:
         return redirect(user_home_url())

    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute('SELECT user_id, username, password_hash, role FROM user WHERE username = %s;', (username,))
            account = cursor.fetchone()
            
            if account and flask_bcrypt.check_password_hash(account['password_hash'], password):
                session.clear()
                session['loggedin'] = True
                session['user_id'] = account['user_id']
                session['username'] = account['username']
                session['role'] = account['role']

                return redirect(user_home_url())
            else:
                flash("Invalid username or password.", "danger")
                return redirect(url_for('user.login'))

    return render_template('login.html')

@user_bp.route('/signup', methods=['GET','POST'])
def signup():
    if 'loggedin' in session:
         return redirect(user_home_url())
    

    form_data = {
        'username': '', 'email': '', 'full_name': '', 'university': '', 'course': ''
    }
    error_data = {
        'username_error': None, 'email_error': None, 'password_error': None
    }

    if request.method == 'POST':

        form_data['username'] = request.form.get('username', '').strip()
        form_data['email'] = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm', '')
        form_data['full_name'] = request.form.get('full_name', '').strip()
        form_data['university'] = request.form.get('university', '').strip()
        form_data['course'] = request.form.get('course', '').strip()

        db_conn = get_db()
        with db_conn.cursor(dictionary=True) as cursor:
            cursor.execute('SELECT user_id FROM user WHERE username = %s;', (form_data['username'],))
            if cursor.fetchone():
                error_data['username_error'] = 'An account already exists with this username.'
            
            cursor.execute('SELECT user_id FROM user WHERE email = %s;', (form_data['email'],))
            if cursor.fetchone():
                error_data['email_error'] = 'An account already exists with this email address.'
        
        if password != confirm_password:
            error_data['password_error'] = "Passwords do not match."
        else:
            is_strong, message = is_password_strong(password)
            if not is_strong:
                error_data['password_error'] = message
        
        if any(error_data.values()):
            return render_template('signup.html', **form_data, **error_data)


        profile_image_file = request.files.get('profile_image')
        resume_pdf_file = request.files.get('resume_pdf')
        
        profile_image_filename = None
        resume_pdf_filename = None
        
        upload_folder = current_app.config.get('UPLOAD_FOLDER')

        
        password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')
        
        with db_conn.cursor() as cursor:
            sql_user = "INSERT INTO `user` (`username`, `password_hash`, `email`, `role`, `status`, `full_name`, `profile_image`) VALUES (%s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(sql_user, (
                form_data['username'], password_hash, form_data['email'], 
                DEFAULT_USER_ROLE, 'active', form_data['full_name'], profile_image_filename
            ))
            
            new_user_id = cursor.lastrowid
            
            if new_user_id:
                sql_student = "INSERT INTO `student` (`user_id`, `university`, `course`, `resume_path`) VALUES (%s, %s, %s, %s);"
                cursor.execute(sql_student, (
                    new_user_id, form_data['university'], form_data['course'], resume_pdf_filename
                ))
            
            db_conn.commit()
            
        flash("Signup successful! Please log in.", "success")
        return redirect(url_for('user.login'))

    return render_template('signup.html', **form_data, **error_data)


@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_id = session['user_id']
    role = session['role']
    db_conn = get_db()
    

    if request.method == 'POST':

        full_name = request.form.get('full_name', '').strip()
        with db_conn.cursor() as cursor:
            cursor.execute("UPDATE user SET full_name = %s WHERE user_id = %s", (full_name, user_id))
        
        if role == 'student':
            university = request.form.get('university', '').strip()
            course = request.form.get('course', '').strip()
            with db_conn.cursor() as cursor:
                cursor.execute("UPDATE student SET university = %s, course = %s WHERE user_id = %s", (university, course, user_id))

            resume_file = request.files.get('resume')
            if resume_file and resume_file.filename != '':
                if not resume_file.filename.lower().endswith('.pdf'):
                    flash("Resume must be a PDF file.", "danger")
                else:
                    filename = secure_filename(f"resume_{user_id}.pdf")
                    upload_folder = os.path.join(current_app.root_path, 'static', 'resumes')
                    os.makedirs(upload_folder, exist_ok=True)
                    resume_path = os.path.join(upload_folder, filename)
                    resume_file.save(resume_path)
                    
                    resume_url_for_db = f'static/resumes/{filename}'
                    with db_conn.cursor() as cursor:
                        cursor.execute("UPDATE student SET resume_path = %s WHERE user_id = %s", (resume_url_for_db, user_id))
                    flash("Resume updated successfully.", "info")

        elif role == 'employer':
            company_name = request.form.get('company_name', '').strip()
            company_description = request.form.get('company_description', '').strip()
            company_website = request.form.get('company_website', '').strip()
            with db_conn.cursor() as cursor:
                cursor.execute("UPDATE employer SET company_name = %s, company_description = %s, company_website = %s WHERE user_id = %s", 
                               (company_name, company_description, company_website, user_id))
            
            logo_file = request.files.get('company_logo')
            if logo_file and logo_file.filename != '':
                allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
                file_ext = logo_file.filename.rsplit('.', 1)[1].lower()
                if file_ext not in allowed_extensions:
                    flash("Invalid image file type for logo.", "danger")
                else:
                    filename = secure_filename(f"logo_{user_id}.{file_ext}")
                    upload_folder = os.path.join(current_app.root_path, 'static', 'logos')
                    os.makedirs(upload_folder, exist_ok=True)
                    logo_path = os.path.join(upload_folder, filename)
                    logo_file.save(logo_path)

                    logo_url_for_db = f'static/logos/{filename}'
                    with db_conn.cursor() as cursor:
                        cursor.execute("UPDATE employer SET company_logo = %s WHERE user_id = %s", (logo_url_for_db, user_id))
                    flash("Company logo updated successfully.", "info")

        db_conn.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for('user.profile'))

    profile_data = None
    with db_conn.cursor(dictionary=True) as cursor:
        if role == 'student':
            cursor.execute("SELECT u.user_id, u.username, u.email, u.full_name, s.university, s.course, s.resume_path FROM user u LEFT JOIN student s ON u.user_id = s.user_id WHERE u.user_id = %s", (user_id,))
            profile_data = cursor.fetchone()
        
        elif role == 'employer':
            cursor.execute("SELECT u.user_id, u.username, u.email, u.full_name, e.company_name, e.company_description, e.company_website, e.company_logo FROM user u LEFT JOIN employer e ON u.user_id = e.user_id WHERE u.user_id = %s", (user_id,))
            profile_data = cursor.fetchone()

        elif role == 'admin':
            cursor.execute("SELECT user_id, username, email, full_name FROM user WHERE user_id = %s", (user_id,))
            profile_data = cursor.fetchone()

    if not profile_data:
        flash("Could not retrieve profile data.", "danger")
        return redirect(url_for('user.root'))

    return render_template('profile.html', profile=profile_data)

    profile_data = None
    with db_conn.cursor(dictionary=True) as cursor:
        if role == 'student':
            cursor.execute("""
                SELECT u.user_id, u.username, u.email, u.full_name, s.university, s.course, s.resume_path
                FROM user u
                LEFT JOIN student s ON u.user_id = s.user_id
                WHERE u.user_id = %s
            """, (user_id,))
            profile_data = cursor.fetchone()
        
        elif role == 'employer':
            cursor.execute("""
                SELECT u.user_id, u.username, u.email, u.full_name, e.company_name, e.company_description, e.company_website, e.company_logo
                FROM user u
                LEFT JOIN employer e ON u.user_id = e.user_id
                WHERE u.user_id = %s
            """, (user_id,))
            profile_data = cursor.fetchone()

        elif role == 'admin':
            cursor.execute("SELECT user_id, username, email, full_name FROM user WHERE user_id = %s", (user_id,))
            profile_data = cursor.fetchone()

    if not profile_data:
        flash("Could not retrieve profile data.", "danger")
        return redirect(url_for('user.root'))

    return render_template('profile.html', profile=profile_data)

@user_bp.route('/logout')
def logout():
    """Logout endpoint."""
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('user.login'))

@user_bp.route('/access_denied')
@login_required
def access_denied():
    """Renders a generic 'access denied' page."""
    return render_template('access_denied.html')

@user_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        user_id = session['user_id']
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        db_conn = get_db()
        with db_conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT password_hash FROM user WHERE user_id = %s", (user_id,))
            user = cursor.fetchone()

        if not user:
            flash("User not found.", "danger")
            return redirect(url_for('user.logout'))

        if not flask_bcrypt.check_password_hash(user['password_hash'], current_password):
            flash("Your current password was incorrect.", "danger")
            return redirect(url_for('user.change_password'))
        
        if new_password != confirm_password:
            flash("New passwords do not match.", "danger")
            return redirect(url_for('user.change_password'))
            
        if new_password == current_password:
            flash("New password cannot be the same as the current password.", "danger")
            return redirect(url_for('user.change_password'))

        is_strong, message = is_password_strong(new_password)
        if not is_strong:
            
            flash(message, "danger")
            return redirect(url_for('user.change_password'))
        
      
        new_password_hash = flask_bcrypt.generate_password_hash(new_password).decode('utf-8')
        with db_conn.cursor() as cursor:
            cursor.execute("UPDATE user SET password_hash = %s WHERE user_id = %s", (new_password_hash, user_id))
        db_conn.commit()

        flash("Your password has been updated successfully.", "success")
        return redirect(url_for('user.profile'))

    return render_template('change_password.html')