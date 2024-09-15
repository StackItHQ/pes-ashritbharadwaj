from flask import Flask, jsonify, request
from models import db, Customer
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize SQLAlchemy
db.init_app(app)

# @app.before_first_request
def create_tables():
    db.create_all()

# Routes for CRUD operations

# Get all students
@app.route('/api/students', methods=['GET'])
def get_students():
    students = Customer.query.all()  # Query the 'students' table
    return jsonify([{
        'ID': s.ID,
        'Name': s.Name,
        'Section': s.Section,
        'College': s.College,
        'RollNumber': s.RollNumber
    } for s in students])

# Get student by ID
@app.route('/api/students/<int:id>', methods=['GET'])
def get_student(id):
    student = Customer.query.get_or_404(id)  # Fetch a specific student by ID
    return jsonify({
        'ID': student.ID,
        'Name': student.Name,
        'Section': student.Section,
        'College': student.College,
        'RollNumber': student.RollNumber
    })

# Create a new student
@app.route('/api/students', methods=['POST'])
def create_student():
    data = request.get_json()
    new_student = Customer(
        Name=data['Name'],
        Section=data['Section'],
        College=data['College'],
        RollNumber=data['RollNumber']
    )
    db.session.add(new_student)
    db.session.commit()
    return jsonify({'ID': new_student.ID}), 201

@app.route('/api/students/bulk', methods=['POST'])
def create_multiple_students():
    data = request.get_json()

    # Debugging: Print out the received data to see its structure
    print("Received data:", data)

    # Check if the data is a list
    if not isinstance(data, list):
        return jsonify({'error': 'Invalid data format. Expected a list of JSON objects.'}), 400

    try:
        # Create a list to store new Customer objects
        new_students = []
        for student_data in data:
            # Validate each object in the list
            new_student = Customer(
                Name=student_data['Name'],
                Section=student_data['Section'],
                College=student_data['College'],
                RollNumber=student_data['RollNumber']
            )
            new_students.append(new_student)
        
        # Add all students at once to the session
        db.session.bulk_save_objects(new_students)
        db.session.commit()

        return jsonify({'message': 'Students added successfully'}), 201

    except KeyError as e:
        return jsonify({'error': f'Missing field in request: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()  # Roll back in case of any error
        return jsonify({'error': str(e)}), 500


# Update student
@app.route('/api/students/<int:id>', methods=['PUT'])
def update_student(id):
    student = Customer.query.get_or_404(id)
    data = request.get_json()
    student.Name = data['Name']
    student.Section = data['Section']
    student.College = data['College']
    student.RollNumber = data['RollNumber']
    db.session.commit()
    return jsonify({'message': 'Student updated successfully'})

# Delete student
@app.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Customer.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student deleted successfully'}), 204

if __name__ == '__main__':
    app.run(debug=True)
