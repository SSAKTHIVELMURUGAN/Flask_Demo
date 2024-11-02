from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
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
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('name', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
