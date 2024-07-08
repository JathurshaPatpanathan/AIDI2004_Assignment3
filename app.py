import sqlite3
from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)


def db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            dob DATE NOT NULL,
            amount_due REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


init_db()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/students', methods=['GET', 'POST'])
def create_student():
    if request.method == 'POST':
        new_student = request.form
        first_name = new_student['first_name']
        last_name = new_student['last_name']
        dob = new_student['dob']
        amount_due = new_student['amount_due']

        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO students (first_name, last_name, dob, amount_due)
            VALUES (?, ?, ?, ?)
        ''', (first_name, last_name, dob, amount_due))
        conn.commit()
        conn.close()

        return redirect(url_for('show_students'))
    return render_template('create.html')


@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM students WHERE student_id = ?', (student_id,))
    student = cursor.fetchone()
    conn.close()

    if student is None:
        return "Student not found", 404

    student_dict = {
        'student_id': student['student_id'],
        'first_name': student['first_name'],
        'last_name': student['last_name'],
        'dob': student['dob'],
        'amount_due': student['amount_due']
    }

    return jsonify(student_dict)


@app.route('/students/<int:student_id>', methods=['GET', 'POST'])
def update_student(student_id):
    conn = db_connection()
    cursor = conn.cursor()

    # Fetch the existing student record
    cursor.execute(
        'SELECT * FROM students WHERE student_id = ?', (student_id,))
    student = cursor.fetchone()

    if student is None:
        return "Student not found", 404

    if request.method == 'POST':
        updated_fields = request.form

        # Prepare updated values, keeping existing ones if not provided in the request
        first_name = updated_fields.get('first_name', student['first_name'])
        last_name = updated_fields.get('last_name', student['last_name'])
        dob = updated_fields.get('dob', student['dob'])
        amount_due = updated_fields.get('amount_due', student['amount_due'])

        cursor.execute('''
            UPDATE students
            SET first_name = ?, last_name = ?, dob = ?, amount_due = ?
            WHERE student_id = ?
        ''', (first_name, last_name, dob, amount_due, student_id))

        conn.commit()
        conn.close()

        return redirect(url_for('show_students'))

    return render_template('update.html', student=student)


@app.route('/students/delete/<int:student_id>', methods=['GET'])
def delete_student(student_id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('show_students'))


@app.route('/students', methods=['GET'])
def show_students():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    conn.close()

    students_list = []
    for student in students:
        student_dict = {
            'student_id': student['student_id'],
            'first_name': student['first_name'],
            'last_name': student['last_name'],
            'dob': student['dob'],
            'amount_due': student['amount_due']
        }
        students_list.append(student_dict)

    return render_template('show.html', students=students_list)


if __name__ == '__main__':
    app.run(debug=True)
