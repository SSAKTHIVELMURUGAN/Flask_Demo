from flask import Flask, render_template, url_for, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = 'localhost'
app.config["MYSQL_USER"] = 'root'
app.config["MYSQL_PASSWORD"] = 'Password'
app.config["MYSQL_DB"] = 'crud' #table name
app.config["MYSQL_CURSORCLASS"] = 'DictCursor'
mysql = MySQL(app)

@app.route("/")
def home():
    con = mysql.connection.cursor()
    sql = "SELECT * FROM users"
    con.execute(sql)
    res = con.fetchall()
    return render_template("home.html", datas=res)

# New User
@app.route("/addUser", methods=['GET', 'POST'])
def addUser():
    if request.method == 'POST':
        name = request.form['Username']
        city = request.form['city']
        age = request.form['age']
        con = mysql.connection.cursor()
        sql = "INSERT INTO users (Username, city, age) VALUES (%s, %s, %s)"
        con.execute(sql, [name, city, age])
        mysql.connection.commit()
        con.close()
        return redirect(url_for("home"))
    return render_template("addUser.html")

# Update User
@app.route("/updateUser/<string:id>", methods=['GET', 'POST'])
def UpdateUser(id):
    con = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form['Username']
        city = request.form['city']
        age = request.form['age']
        sql = "UPDATE users SET Username=%s, city=%s, age=%s WHERE id=%s"
        con.execute(sql, [name, city, age, id])
        mysql.connection.commit()
        con.close()
        return redirect(url_for("home"))
    else:
        sql = "SELECT * FROM users WHERE id = %s"
        con.execute(sql, [id])
        res = con.fetchone()
        con.close()
        return render_template("UpdateUser.html", datas=res)

# Delete User
@app.route("/deleteUser/<string:id>", methods=['GET', 'POST'])
def deleteUser(id):
    con = mysql.connection.cursor()
    sql = "DELETE FROM users WHERE id = %s"
    con.execute(sql, [id])
    mysql.connection.commit()
    con.close()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
