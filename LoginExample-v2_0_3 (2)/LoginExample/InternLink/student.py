import os
import time
from flask import Blueprint, redirect, render_template, session, url_for, request, flash, current_app
from werkzeug.utils import secure_filename
from .utils import login_required, role_required
from .db import get_db

student_bp = Blueprint('student', __name__, url_prefix='/student')

@student_bp.route('/home')
@login_required
@role_required('student')
def student_home():
    db_conn = get_db()
    with db_conn.cursor(dictionary=True) as cursor:
        username = session['username']
        cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
        user = cursor.fetchone()
    return render_template('student_home.html', user=user)

@student_bp.route('/internships')
@login_required
@role_required('student')
def browse_internships():
    db_conn = get_db()
    with db_conn.cursor(dictionary=True) as cursor:
        search_query = request.args.get('search', '')
        location_query = request.args.get('location', '')
        category_query = request.args.get('category', '')
        duration_query = request.args.get('duration', '')

        query = "SELECT i.*, e.company_name FROM internship i JOIN employer e ON i.company_id = e.emp_id WHERE 1=1"
        params = []

        if search_query.strip():
            query += " AND (i.title LIKE %s OR e.company_name LIKE %s)"
            params.extend([f"%{search_query}%", f"%{search_query}%"])
        if location_query.strip():
            query += " AND i.location LIKE %s"
            params.append(f"%{location_query}%")
        if category_query.strip():
            query += " AND i.category = %s"
            params.append(category_query)
        if duration_query.strip():
            query += " AND i.duration = %s"
            params.append(duration_query)
        
        query += " ORDER BY i.deadline DESC"

        cursor.execute(query, tuple(params))
        internships = cursor.fetchall()
    
    return render_template('browse_internships.html', 
                           internships=internships, 
                           search=search_query, 
                           location=location_query, 
                           category=category_query, 
                           duration=duration_query)

@student_bp.route('/apply/<int:internship_id>', methods=['GET', 'POST'])
@login_required
@role_required('student')
def apply_internship(internship_id):
    db_conn = get_db()
    user_id = session['user_id']
    
    with db_conn.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT student_id FROM student WHERE user_id = %s", (user_id,))
        student_profile = cursor.fetchone()
    
    if not student_profile:
        flash("Could not find your student profile.", "danger")
        return redirect(url_for('student.student_home'))
    
    student_id = student_profile['student_id']
    
    with db_conn.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT application_id FROM application WHERE student_id = %s AND internship_id = %s", (student_id, internship_id))
        existing_application = cursor.fetchone()
    if existing_application:
        flash('You have already applied for this internship.', 'info')
        return redirect(url_for('student.my_applications'))

    if request.method == 'GET':
        with db_conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT i.*, e.company_name FROM internship i JOIN employer e ON i.company_id = e.emp_id WHERE i.internship_id = %s", (internship_id,))
            internship = cursor.fetchone()
            if not internship:
                flash('Internship not found.', 'danger')
                return redirect(url_for('student.browse_internships'))
            sql_student_info = "SELECT u.full_name, u.email, s.university, s.course FROM user u JOIN student s ON u.user_id = s.user_id WHERE u.user_id = %s"
            cursor.execute(sql_student_info, (user_id,))
            student_display_info = cursor.fetchone()
        return render_template('apply_internship.html', internship=internship, student=student_display_info)

    if request.method == 'POST':
        cover_letter = request.form.get('cover_letter')
        resume_file = request.files.get('resume')
        if not resume_file or resume_file.filename == '':
            flash('Resume file is required.', 'danger')
            return redirect(request.url)
        if not resume_file.filename.lower().endswith('.pdf'):
            flash('Only PDF files are allowed.', 'danger')
            return redirect(request.url)
        
        filename = secure_filename(resume_file.filename)
        unique_filename = f"{student_id}_{int(time.time())}_{filename}"
        upload_folder = os.path.join(current_app.root_path, 'static', 'resumes')
        os.makedirs(upload_folder, exist_ok=True)
        resume_path = os.path.join(upload_folder, unique_filename)
        resume_file.save(resume_path)
        resume_url_for_db = f'static/resumes/{unique_filename}'

        try:
            with db_conn.cursor() as cursor:
               
                sql = """
                    INSERT INTO application 
                    (student_id, internship_id, status, cover_letter, resume_url, application_date) 
                    VALUES (%s, %s, 'pending', %s, %s, NOW())
                """
                cursor.execute(sql, (student_id, internship_id, cover_letter, resume_url_for_db))
            db_conn.commit()
            flash('Application submitted successfully!', 'success')
            return redirect(url_for('student.my_applications'))
        except Exception as e:
            db_conn.rollback()
            flash(f'An error occurred: {e}', 'danger')
            if os.path.exists(resume_path):
                os.remove(resume_path)
            return redirect(request.url)
        
@student_bp.route('/my_applications')
@login_required
@role_required('student')
def my_applications():
    db_conn = get_db()
    user_id = session['user_id']

    with db_conn.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT student_id FROM student WHERE user_id = %s", (user_id,))
        student_profile = cursor.fetchone()
    
    if not student_profile:
        return render_template('my_applications.html', applications=[])
    
    student_id = student_profile['student_id']
    
    with db_conn.cursor(dictionary=True) as cursor:
        
        sql = """
            SELECT 
                a.application_id, a.status, a.feedback, a.application_date,
                i.title AS internship_title, e.company_name
            FROM application a
            JOIN internship i ON a.internship_id = i.internship_id
            JOIN employer e ON i.company_id = e.emp_id
            WHERE a.student_id = %s
            ORDER BY a.application_date DESC
        """
        cursor.execute(sql, (student_id,))
        applications = cursor.fetchall()
        
    return render_template('my_applications.html', applications=applications)