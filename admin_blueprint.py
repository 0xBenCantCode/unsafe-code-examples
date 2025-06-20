from flask import Blueprint, session, request, render_template_string
import sqlite3
import os

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/dashboard')
def dashboard():
    # VULNERABILITY 11: Missing authorization check
    # Should check if user has admin role, but doesn't
    
    return '''
    <h2>Admin Dashboard</h2>
    <p>Welcome to admin area!</p>
    <form action="/admin/execute" method="post">
        <input type="text" name="command" placeholder="Enter command">
        <input type="submit" value="Execute">
    </form>
    '''

@admin_bp.route('/execute', methods=['POST'])
def execute_command():
    # VULNERABILITY 12: Command injection
    command = request.form['command']
    result = os.system(command)  # Extremely dangerous!
    return f"Command executed with result: {result}"

@admin_bp.route('/users')
def list_users():
    # VULNERABILITY 13: Information disclosure
    conn = sqlite3.connect('app.db')
    users = conn.execute("SELECT username, password, role FROM users").fetchall()
    conn.close()
    
    # Exposing passwords in plain text
    user_list = "<h2>All Users:</h2>"
    for user in users:
        user_list += f"<p>User: {user[0]}, Password: {user[1]}, Role: {user[2]}</p>"
    
    return user_list

@admin_bp.route('/template')
def custom_template():
    # VULNERABILITY 14: More SSTI in blueprint
    template_code = request.args.get('template', '<h1>Default</h1>')
    return render_template_string(template_code)
