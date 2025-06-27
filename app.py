from flask import Flask,render_template, request, redirect, session, url_for
import sqlite3
app = Flask(__name__)
app.secret_key = 'your_secret_key'

def init_db():
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                  id INTEGER PRIMARY KEY,
                  username TEXT,
                  password TEXT,
                  role TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXCITS students (
                  id INTEGER PRIMARY KEY,
                  name TEXT,
                  class TEXT,
                  roll_no TEXT,
                  dob TEXT,
                  address TEXT,
                  parent_context TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXCITS attendance (
                  id INTEGER PRIMARY KEY,
                  student_id INTEGER,
                  date TEXT,
                  status TEXT,
                  FOREIGN KEY(student_id) REFERENCE students(id))''')
        conn.commit()

@app.route('/')
def home():
    return redirect(url_for('login'))
@app.route('/login', methods=['GET','POST'])
def login():
    error = ''
    if request.method == 'post':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE username=? AND password=?",(username, password))
            user = c.fetchone()
            if user:
                session['user_id'] = user[0]
                session['role'] = user[3]
                return redirect(url_for('dasboard'))
            else:
                error = "Invalid credentials"
    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    if 'role' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html',role=session['role'])

@app.route('/register_student',methods=['GET','POST'])
def register_student():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    if request.method == 'POST':
        data = (request.form['name'], request.form['class'], request.form['roll_no'],
                request.form['dob'], request.form['address'], request.form['parent_contact'])
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute('''INSERT INTO students (name, class, roll_no, dob, address, parent_contact) VALUES (?, ?, ?, ?, ?, ?)''', data)
            conn.commit()
        return redirect(url_for('dashboard'))
    return render_template('register_student.html')

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if 'role' not in session or session['role'] != 'teacher':
        return redirect(url_for('login'))
    with sqlite3.connect()