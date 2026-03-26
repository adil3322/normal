
from flask import Flask, render_template, request, jsonify, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

def init_db():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, name TEXT, course TEXT)')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    if 'user' not in session:
        return redirect('/login')
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        data = request.form
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (data['username'], data['password']))
        user = c.fetchone()
        conn.close()
        if user:
            session['user'] = data['username']
            return redirect('/')
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        data = request.form
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()
        c.execute("INSERT INTO users (username,password) VALUES (?,?)", (data['username'], data['password']))
        conn.commit()
        conn.close()
        return redirect('/login')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/add', methods=['POST'])
def add_student():
    data = request.json
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("INSERT INTO students (name,course) VALUES (?,?)", (data['name'], data['course']))
    conn.commit()
    conn.close()
    return jsonify({"msg":"added"})

@app.route('/get')
def get_students():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    data = [{"id":r[0],"name":r[1],"course":r[2]} for r in c.fetchall()]
    conn.close()
    return jsonify(data)

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"msg":"deleted"})

if __name__ == "__main__":
    app.run(debug=True)
