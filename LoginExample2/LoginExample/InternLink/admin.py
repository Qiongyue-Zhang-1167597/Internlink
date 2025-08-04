from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_from_directory, current_app
from .utils import login_required, role_required
from .db import get_db
import os  
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/home', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def admin_home():
    db_conn = get_db()
    username = session['username']
    print("Debug: Session data:", session)  

    with db_conn.cursor(dictionary=True) as cursor:
       
        cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
        user = cursor.fetchone()
        print("Debug: Queried user:", user)  
        
        if not user:
            flash("User not found.", "danger")
            return redirect(url_for('login'))

        if request.method == 'POST':
            full_name = request.form.get('full_name', user['full_name'])
            email = request.form.get('email', user['email'])
            print("Debug: POST data:", request.form)
            print("Debug: New values - full_name:", full_name, "email:", email)
            print("Debug: Old values - full_name:", user['full_name'], "email:", user['email'])
            
            if email != user['email']:
                cursor.execute("SELECT user_id FROM user WHERE email = %s AND user_id != %s", (email, user['user_id']))
                if cursor.fetchone():
                    flash('Email already in use.', 'danger')
                    return render_template('admin_home.html', user=user)
            
           
            update_query = "UPDATE user SET full_name = %s, email = %s WHERE user_id = %s"
            cursor.execute(update_query, (full_name, email, user['user_id']))
            db_conn.commit()
            print("Debug: Update rowcount:", cursor.rowcount)
            print("Debug: Updated with user_id:", user['user_id'])
            
            
            cursor.execute("SELECT * FROM user WHERE user_id = %s", (user['user_id'],))
            updated_user = cursor.fetchone()
            print("Debug: Updated user from db:", updated_user)  
            
            if cursor.rowcount > 0:
                flash('Profile updated successfully!', 'success')
                user = updated_user  
            elif full_name == user['full_name'] and email == user['email']:
                flash('No changes were made (values are the same).', 'info')
            else:
                flash('Update failed (rowcount=0). Check if user_id matches db: ' + str(user['user_id']), 'warning')
            
            return redirect(url_for('admin.admin_home'))  
    
    return render_template('admin_home.html', user=user)

@admin_bp.route('/users')
@login_required
@role_required('admin')
def view_users():
    """Administrators can view the list page of all users, which supports filtering."""
    search_name = request.args.get('name', '').strip()
    filter_role = request.args.get('role', '').strip()
    filter_status = request.args.get('status', '').strip()

    query = "SELECT `user_id`, `username`, `full_name`, `email`, `role`, `status` FROM `user` WHERE 1=1"
    params = []

    if search_name:
        query += " AND `full_name` LIKE %s"
        params.append(f"%{search_name}%")
    
    if filter_role:
        query += " AND `role` = %s"
        params.append(filter_role)

    if filter_status:
        query += " AND `status` = %s"
        params.append(filter_status)
    
    query += " ORDER BY `user_id` ASC;"

    db_conn = get_db()
    with db_conn.cursor(dictionary=True) as cursor:
        cursor.execute(query, tuple(params))
        users_list = cursor.fetchall()
    
    return render_template('admin_view_users.html', 
                           users=users_list, 
                           search_name=search_name,
                           filter_role=filter_role,
                           filter_status=filter_status)

@admin_bp.route('/users/toggle_status/<int:user_id>', methods=['POST'])
@login_required
@role_required('admin')
def toggle_user_status(user_id):
    """切换用户的 active/inactive 状态。"""
    if user_id == session.get('user_id'): 
        flash("You cannot change your own status.", "danger")
        return redirect(url_for('admin.view_users'))

    db_conn = get_db()
    with db_conn.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT `status` FROM `user` WHERE `user_id` = %s", (user_id,))
        user = cursor.fetchone()
        
        if user:
            new_status = 'inactive' if user['status'] == 'active' else 'active'
            cursor.execute("UPDATE `user` SET `status` = %s WHERE `user_id` = %s", (new_status, user_id))
            db_conn.commit()
            flash(f"User status for user ID {user_id} has been updated to {new_status}.", "success")
        else:
            flash("User not found.", "danger")
            
    return redirect(url_for('admin.view_users')) 

@admin_bp.route('/internships')
@login_required
@role_required('admin')
def view_all_internships():
    """Admin View all internship pages, supporting complete filtering."""
    db_conn = get_db()
    with db_conn.cursor(dictionary=True) as cursor:
        search_query = request.args.get('search', '')
        location_query = request.args.get('location', '')
        category_query = request.args.get('category', '')
        duration_query = request.args.get('duration', '')

        query = """
            SELECT i.*, e.company_name 
            FROM internship i
            JOIN employer e ON i.company_id = e.emp_id
            WHERE 1=1
        """
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

@admin_bp.route('/applications')
@login_required
@role_required('admin')
def view_all_applications():
    """Admin View all student applications page, with search/filter support."""
    db_conn = get_db()
    with db_conn.cursor(dictionary=True) as cursor:
       
        search_student = request.args.get('search_student', '').strip()
        search_company = request.args.get('search_company', '').strip()
        filter_status = request.args.get('filter_status', '').strip()

        sql = """
            SELECT 
                a.*,  -- includeresume_url
                u.full_name,
                i.title AS internship_title,
                e.company_name,
                a.resume_url  -- select resume_url（optional，but make sure）
            FROM application a
            JOIN student s ON a.student_id = s.student_id
            JOIN user u ON s.user_id = u.user_id
            JOIN internship i ON a.internship_id = i.internship_id
            JOIN employer e ON i.company_id = e.emp_id
            WHERE 1=1
        """
        params = []

        if search_student:
            sql += " AND u.full_name LIKE %s"
            params.append(f"%{search_student}%")

        if search_company:
            sql += " AND e.company_name LIKE %s"
            params.append(f"%{search_company}%")

        if filter_status:
            sql += " AND a.status = %s"
            params.append(filter_status)

        sql += " ORDER BY a.application_date DESC"
        
        cursor.execute(sql, tuple(params))
        applications = cursor.fetchall()

   
    status_options = ['', 'pending', 'accepted', 'short listed', 'rejected']  

    return render_template('admin_view_applications.html', 
                           applications=applications,
                           search_student=search_student,
                           search_company=search_company,
                           filter_status=filter_status,
                           status_options=status_options)

@admin_bp.route('/download_resume/<path:filename>')
@login_required
@role_required('admin')
def download_resume(filename):
    
    resumes_dir = os.path.join(current_app.root_path, 'static', 'resumes')  
    return send_from_directory(resumes_dir, filename, as_attachment=False)  