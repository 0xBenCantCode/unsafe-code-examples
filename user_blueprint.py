# user_blueprint.py - User-related routes
from flask import Blueprint, session, request, redirect, url_for
import sqlite3

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # VULNERABILITY 8: No proper access control
    user_id = request.args.get('id', session['user_id'])
    
    # VULNERABILITY 9: SQL Injection in blueprint
    conn = sqlite3.connect('app.db')
    query = f"SELECT username, role FROM users WHERE id={user_id}"
    result = conn.execute(query).fetchone()
    conn.close()
    
    if result:
        return f"<h2>Profile</h2><p>Username: {result[0]}</p><p>Role: {result[1]}</p>"
    return "User not found"

@user_bp.route('/update', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # VULNERABILITY 10: No CSRF protection
    new_username = request.form['username']
    user_id = session['user_id']
    
    conn = sqlite3.connect('app.db')
    # Another SQL injection point
    query = f"UPDATE users SET username='{new_username}' WHERE id={user_id}"
    conn.execute(query)
    conn.commit()
    conn.close()
    
    return "Profile updated"
