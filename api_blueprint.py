from flask import Blueprint, request, jsonify, session
import sqlite3

api_bp = Blueprint('api_bp', __name__)

@api_bp.route('/users', methods=['GET'])
def get_users():
    # VULNERABILITY 15: No authentication for API
    # VULNERABILITY 16: No rate limiting
    
    conn = sqlite3.connect('app.db')
    users = conn.execute("SELECT id, username, role FROM users").fetchall()
    conn.close()
    
    return jsonify([{"id": u[0], "username": u[1], "role": u[2]} for u in users])

@api_bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # VULNERABILITY 17: No authorization for destructive operations
    conn = sqlite3.connect('app.db')
    conn.execute(f"DELETE FROM users WHERE id={user_id}")
    conn.commit()
    conn.close()
    
    return jsonify({"message": "User deleted"})

@api_bp.route('/search')
def search_users():
    # VULNERABILITY 18: SQL injection in API
    query = request.args.get('q', '')
    
    conn = sqlite3.connect('app.db')
    sql = f"SELECT username FROM users WHERE username LIKE '%{query}%'"
    results = conn.execute(sql).fetchall()
    conn.close()
    
    return jsonify([r[0] for r in results])

@api_bp.route('/upload', methods=['POST'])
def upload_file():
    # VULNERABILITY 19: Unrestricted file upload
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400
    
    file = request.files['file']
    if file.filename:
        # No validation of file type or content
        file.save(f"uploads/{file.filename}")
        return jsonify({"message": "File uploaded successfully"})
    
    return jsonify({"error": "Invalid file"}), 400
