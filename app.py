from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'secret123'

# Sample course data (you can connect to SQLite later)
courses = {
    1: {"id": 1, "name": "IIT-JEE", "description": "Engineering Entrance Coaching", "total_slots": 50, "available_slots": 10, "fee": 85000},
    2: {"id": 2, "name": "NEET", "description": "Medical Entrance Coaching", "total_slots": 40, "available_slots": 12, "fee": 78000},
    3: {"id": 3, "name": "Class 6-10 Foundation", "description": "Strong fundamentals for school students", "total_slots": 60, "available_slots": 25, "fee": 40000}
}

admission_data = {}

@app.route('/')
def home():
    return render_template('index.html', courses=courses.values())

@app.route('/course/<int:course_id>')
def course_details(course_id):
    course = courses.get(course_id)
    return render_template('course_detail.html', course=course)

@app.route('/admission/<int:course_id>', methods=['GET', 'POST'])
def admission(course_id):
    course = courses.get(course_id)
    if request.method == 'POST':
        admission_data['student_name'] = request.form['student_name']
        admission_data['email'] = request.form['email']
        admission_data['phone'] = request.form['phone']
        admission_data['payment_status'] = "Pending"
        return redirect(url_for('payment', course_id=course_id))
    return render_template('admission.html', course=course)

@app.route('/payment/<int:course_id>', methods=['GET', 'POST'])
def payment(course_id):
    course = courses.get(course_id)
    if request.method == 'POST':
        admission_data['payment_status'] = "Paid"
        flash("✅ Payment Successful!", "success")
        return redirect(url_for('confirmation', course_id=course_id))
    return render_template('payment.html', course=course, admission=admission_data)

@app.route('/confirmation/<int:course_id>')
def confirmation(course_id):
    course = courses.get(course_id)
    return render_template('confirmation.html', course=course, admission=admission_data)

if __name__ == '__main__':
    app.run(debug=True)
