from flask import Flask, render_template, request
app=Flask(__name__)

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/home',methods=["POST","GET"])
def confirm():
    if request.method == "POST":
        n=request.form.get('name')
        p=request.form.get('place')
        pn = request.form.get('phone')
        return render_template('home.html',name=n,place=p,phone=pn)
    
if __name__ == "__main__":
    app.run(debug=True)