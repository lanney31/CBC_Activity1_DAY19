from flask import Flask, request, session, redirect, render_template
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL database connection (edit according to your config)
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="flask_app"
)
cursor = db.cursor(dictionary=True)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']

        if password != confirm:
            return "Passwords do not match"

        try:
            cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
            db.commit()
            return redirect('/login')
        except:
            return "Email already registered"
    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()

        if user:
            session['email'] = email
            return redirect('/home')
        else:
            return "Invalid credentials"
    return render_template("login.html")

@app.route('/home')
def home():
    if 'email' not in session:
        return redirect('/login')
    return render_template("home.html", email=session['email'])

@app.route('/add-info', methods=['GET', 'POST'])
def add_info():
    if 'email' not in session:
        return redirect('/login')
    if request.method == 'POST':
        data = (
            session['email'],
            request.form['fname'],
            request.form['mname'],
            request.form['lname'],
            request.form['age'],
            request.form['address'],
            request.form['bday']
        )
        cursor.execute('''
            INSERT INTO user_info (email, fname, mname, lname, age, address, bday)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', data)
        db.commit()
        return "Information submitted successfully"
    return render_template("add_info.html")

if __name__ == '__main__':
    app.run(ssl_context='adhoc')
