from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'replace your password'
app.config['MYSQL_DB'] = 'loginsignupdb'

mysql = MySQL(app)

@app.route('/')
def home():
    if 'user_id' in session:
        return render_template('home.html', name=session['name'])
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        
        cur = mysql.connection.cursor()
        
        # Check if the email already exists
        cur.execute("SELECT * FROM userlogindetails WHERE Email = %s", (email,))
        existing_user = cur.fetchone()
        
        if existing_user:
            flash('Error: Email already registered!', 'danger')
            cur.close()
            return redirect(url_for('register'))
        
        # Insert new user if email is unique
        try:
            cur.execute("INSERT INTO userlogindetails (Name, Email, Password) VALUES (%s, %s, %s)", (name, email, password))
            mysql.connection.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except:
            mysql.connection.rollback()
            flash('An error occurred. Please try again.', 'danger')
        finally:
            cur.close()
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM userlogindetails WHERE Email = %s", (email,))
        user = cur.fetchone()
        cur.close()
         
        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            session['name'] = user[1]
            session['email'] = user[2]  # Store email in session
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('name', None)
    session.pop('email', None)  # Remove email from session
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    # Pass user's name and email to the profile template
    if 'name' in session and 'email' in session:
        name = session['name']
        email = session['email']
        return render_template('profile.html', name=name, email=email)
    return redirect(url_for('login'))  # Redirect if not logged in

@app.route('/cgpa_calculator', methods=['GET', 'POST'])
def cgpa_calculator():
    if request.method == 'POST':
        # Fetch form data for calculation
        subjects = int(request.form.get('subjects', 0))
        grades = request.form.getlist('grades')  # assuming list of grades for each subject
        total_credits = 0
        total_points = 0
        for grade in grades:
            points = convert_grade_to_points(grade)
            credits = int(request.form.get(f'credits_{grade}', 1))  # sample credit system
            total_credits += credits
            total_points += points * credits
        cgpa = total_points / total_credits if total_credits else 0
        return render_template('cgpa_calculator.html', cgpa=cgpa)
    return render_template('cgpa_calculator.html')

def convert_grade_to_points(grade):
    grade_to_points = {
        'A': 4.0,
        'B': 3.0,
        'C': 2.0,
        'D': 1.0,
        'F': 0.0
    }
    return grade_to_points.get(grade.upper(), 0)

if __name__ == '__main__':
    app.run(debug=True)
