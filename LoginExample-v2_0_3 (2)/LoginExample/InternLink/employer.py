
from flask import Blueprint, redirect, render_template, session, url_for, flash, request
from .db import get_db
from .utils import login_required, role_required

employer_bp = Blueprint('employer', __name__, url_prefix='/employer')

@employer_bp.route('/home')
@login_required
@role_required('employer')
def employer_home():
    db_conn = get_db()
    with db_conn.cursor(dictionary=True) as cursor:
        username = session['username']
        cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
        user = cursor.fetchone()
    return render_template('employer_home.html', user=user)

@employer_bp.route('/postings')
@login_required
@role_required('employer')
def view_my_postings():
    user_id = session.get('user_id')
    db_conn = get_db()
    
    with db_conn.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT emp_id FROM employer WHERE user_id = %s", (user_id,))
        employer = cursor.fetchone()

        if not employer:
            flash("Employer profile not found.", "danger")
            return redirect(url_for('employer.employer_home'))

        employer_id = employer['emp_id']
        
        sql = """
            SELECT i.*, (SELECT COUNT(*) FROM application a WHERE a.internship_id = i.internship_id) AS applicant_count
            FROM internship i
            WHERE i.company_id = %s
            ORDER BY i.deadline DESC
        """
        cursor.execute(sql, (employer_id,))
        postings = cursor.fetchall()
    
    return render_template('employer_postings.html', postings=postings)

@employer_bp.route('/postings/<int:internship_id>/applicants')
@login_required
@role_required('employer')
def view_applicants(internship_id):
    user_id = session.get('user_id')
    db_conn = get_db()
    
    
    with db_conn.cursor(dictionary=True) as cursor:
       
        cursor.execute("SELECT i.title FROM employer e JOIN internship i ON e.emp_id = i.company_id WHERE e.user_id = %s AND i.internship_id = %s", (user_id, internship_id))
        internship = cursor.fetchone()
        if not internship:
            flash("You do not have permission to view these applicants.", "danger")
            return redirect(url_for('employer.view_my_postings'))

       
        search_name = request.args.get('name', '').strip()
        search_status = request.args.get('status', '').strip()

       
        sql = """
            SELECT u.full_name, u.email, s.university, s.course,
                   a.application_id, a.application_date, a.status, a.resume_url, a.cover_letter
            FROM application a
            JOIN student s ON a.student_id = s.student_id
            JOIN user u ON s.user_id = u.user_id
            WHERE a.internship_id = %s
        """
        params = [internship_id]

        if search_name:
            sql += " AND u.full_name LIKE %s"
            params.append(f"%{search_name}%")
        if search_status:
            sql += " AND a.status = %s"
            params.append(search_status)
        
        sql += " ORDER BY a.application_date DESC"
        
        cursor.execute(sql, tuple(params))
        applicants = cursor.fetchall()
        
    return render_template('employer_view_applicants.html', 
                           applicants=applicants, 
                           internship=internship,
                           internship_id=internship_id,
                           search_name=search_name,
                           search_status=search_status)

@employer_bp.route('/applications/<int:application_id>/status/<new_status>', methods=['POST'])
@login_required
@role_required('employer')
def manage_application_status(application_id, new_status):
    user_id = session.get('user_id')
    db_conn = get_db()


    try:
        with db_conn.cursor(dictionary=True) as cursor:
            
            cursor.execute("""
                SELECT a.internship_id 
                FROM application a
                JOIN internship i ON a.internship_id = i.internship_id
                JOIN employer e ON i.company_id = e.emp_id
                WHERE e.user_id = %s AND a.application_id = %s
            """, (user_id, application_id))
            
            auth_check = cursor.fetchone()
            if not auth_check:
                flash("You do not have permission to modify this application.", "danger")
                return redirect(url_for('employer.view_my_postings'))
            
            allowed_statuses = ['accepted', 'rejected']
            if new_status not in allowed_statuses:
                flash("Invalid status update.", "danger")
                return redirect(request.referrer or url_for('employer.view_my_postings'))

            feedback = request.form.get('feedback', None)

            cursor.execute(
                "UPDATE application SET status = %s, feedback = %s WHERE application_id = %s",
                (new_status, feedback, application_id)
            )
        
        db_conn.commit()
        flash(f"Application has been successfully {new_status}.", "success")

    except Exception as e:
        db_conn.rollback() 
        flash(f"An error occurred: {e}", "danger")

    return redirect(request.referrer or url_for('employer.view_my_postings'))