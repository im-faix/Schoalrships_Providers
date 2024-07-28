from flask import Flask, request, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='scholarship_db'
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_student')
def create_student():
    return render_template('create_student.html')

@app.route('/add_student', methods=['POST'])
def add_student():
    # Collect form data
    name = request.form['name']
    gender = request.form['gender']
    date_of_birth = request.form['date_of_birth']
    income = request.form['income']
    academic_performance = request.form['academic_performance']
    enrollment_status = request.form['enrollment_status']
    student_class = request.form['class']
    institute_name = request.form['institute_name']
    board = request.form['board']
    religion = request.form['religion']
    caste = request.form['caste']
    adhar = request.form['adhar']
    nationality = request.form['nationality']
    special_category = request.form['special_category']

    cursor = connection.cursor()

    query = """
    INSERT INTO students (name, gender, date_of_birth, income, academic_performance, enrollment_status, class, institute_name, board, religion, caste, adhar, nationality, special_category)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (name, gender, date_of_birth, income, academic_performance, enrollment_status, student_class, institute_name, board, religion, caste, adhar, nationality, special_category))
    connection.commit()
    cursor.close()

    return redirect(url_for('index'))

@app.route('/check_scholarship', methods=['POST'])
def check_scholarship():
    student_id = request.form['student_id']
    cursor = connection.cursor()

    # Fetch student data
    cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
    student = cursor.fetchone()

    if student:
        # Fetch scholarships based on student data
        query = """
        SELECT * FROM scholarships
        WHERE income_limit >= %s
        AND academic_performance_min <= %s
        AND (residency_requirement = 'National' OR residency_requirement = %s)
        AND (caste = 'Any' OR caste = %s)
        AND (religion = 'Any' OR religion = %s)
        AND (board = 'Any' OR board = %s)
        AND (gender = 'Any' OR gender = %s)
        AND (special_category = 'Any' OR special_category = %s)
        """
        cursor.execute(query, (student[4], student[5], student[13], student[11], student[10], student[9], student[2], student[14]))
        scholarships = cursor.fetchall()
        cursor.close()

        return render_template('results.html', student=student, scholarships=scholarships)
    else:
        cursor.close()
        return "Student not found", 404

if __name__ == '__main__':
    app.run(debug=True)
