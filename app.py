from flask import Flask, request, render_template_string, session, redirect, url_for
import sqlite3
import os
import pickle
import base64

# Import blueprints
from user_blueprint import user_bp
from admin_blueprint import admin_bp
from api_blueprint import api_bp

app = Flask(__name__)

# VULNERABILITY 1: Weak secret key
app.secret_key = "secret123"

# VULNERABILITY 2: Debug mode enabled
app.config['DEBUG'] = True

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(api_bp, url_prefix='/api')

# VULNERABILITY 3: Insecure database initialization
def init_db():
    conn = sqlite3.connect('app.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS users 
                    (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)''')
    conn.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'password123', 'admin')")
    conn.execute("INSERT OR IGNORE INTO users VALUES (2, 'user', 'user123', 'user')")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    # VULNERABILITY 4: Server-Side Template Injection (SSTI)
    name = request.args.get('name', 'Guest')
    template = f"<h1>Welcome {name}!</h1><p>This is an unsafe Flask app for demonstration.</p>"
    return render_template_string(template)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # VULNERABILITY 5: SQL Injection
        conn = sqlite3.connect('app.db')
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        result = conn.execute(query).fetchone()
        conn.close()
        
        if result:
            session['user_id'] = result[0]
            session['username'] = result[1]
            session['role'] = result[3]
            return redirect(url_for('user_bp.profile'))
        else:
            return "Invalid credentials"
    
    return '''
    <form method="post">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Login">
    </form>
    '''

@app.route('/serialize')
def serialize_data():
    # VULNERABILITY 6: Insecure deserialization
    data = request.args.get('data')
    if data:
        try:
            decoded = base64.b64decode(data)
            obj = pickle.loads(decoded)  # Dangerous deserialization
            return f"Deserialized: {obj}"
        except:
            return "Invalid data"
    return "Provide data parameter"

if __name__ == '__main__':
    init_db()
    # VULNERABILITY 7: Running with host='0.0.0.0' in debug mode
    app.run(host='0.0.0.0', port=5000, debug=True)
