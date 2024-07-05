# Flask CRUD API for Student Records

This project is a simple RESTful API built with Flask for managing student records. The API allows you to perform Create, Read, Update, and Delete (CRUD) operations on a SQLite database.

## Features

- Create a new student record
- Read an existing student record
- Update an existing student record
- Delete an existing student record
- Retrieve all student records

## Endpoints

### Create a Student (POST)
- **URL**: `/students`
- **Method**: `POST`
- **Body**: JSON
  ```json
  {
      "first_name": "Smith",
      "last_name": "Sam",
      "dob": "2000-09-15",
      "amount_due": 3600.00
  }


### Read a Student (GET)
- **URL**: /students/<student_id>
- **Method**: GET

### Update a Student (PATCH)
- **URL**: /students/<student_id>
- **Method**: PATCH

### Delete a Student (DELETE)
- **URL**: /students/<student_id>
- **Method**: DELETE

### Show All Students (GET)
- **URL**: /students
- **Method**: GET

### Project Structure
- **app.py**: Main application file containing the Flask routes and logic.
- **students.db**: SQLite database file (created automatically).
