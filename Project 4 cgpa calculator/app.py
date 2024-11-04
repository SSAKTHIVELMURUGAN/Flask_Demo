from flask import Flask, render_template, request

app = Flask(__name__)

# Function to calculate CGPA
def calculate_cgpa(grades):
    if not grades:
        return 0.0
    total_points = sum(grades)
    return total_points / len(grades)

@app.route('/', methods=['GET', 'POST'])
def index():
    cgpa = None  # Initialize cgpa variable
    if request.method == 'POST':
        # Retrieve form data
        subjects = request.form.getlist('subject')
        grades = request.form.getlist('grade')

        # Convert grades to float
        try:
            grades = [float(grade) for grade in grades if grade.strip()]
            cgpa = calculate_cgpa(grades)  # Calculate CGPA
        except ValueError:
            cgpa = 'Invalid input! Please enter valid grades.'

    return render_template('index.html', cgpa=cgpa)

if __name__ == '__main__':
    app.run(debug=True)
