from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exams.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Database Models ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), unique=True, nullable=False)
    course_name = db.Column(db.String(100), nullable=False)

class Examination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exam_title = db.Column(db.String(100), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

class Mark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('examination.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    grade = db.Column(db.String(5), nullable=False)

# --- Automated Grading Helper ---
def calculate_grade(score):
    if score >= 70:
        return 'A'
    elif score >= 60:
        return 'B'
    elif score >= 50:
        return 'C'
    elif score >= 40:
        return 'D'
    else:
        return 'F'

@app.route('/')
def home():
    return render_template('index.html')

# --- POST Endpoint to Record Mark ---
@app.route('/api/mark', methods=['POST'])
def add_mark():
    data = request.json
    score = float(data['score'])
    grade = calculate_grade(score)
    
    new_mark = Mark(
        student_id=data['student_id'],
        exam_id=data['exam_id'],
        score=score,
        grade=grade
    )
    db.session.add(new_mark)
    db.session.commit()
    return jsonify({"message": "Mark recorded successfully!", "score": score, "grade": grade}), 201

# --- GET Endpoint with Optional Filtering ---
@app.route('/api/marks', methods=['GET'])
def get_marks():
    student_id = request.args.get('student_id')
    
    # Query with optional filter
    if student_id:
        marks = Mark.query.filter_by(student_id=student_id).all()
    else:
        marks = Mark.query.all()
        
    result = []
    for m in marks:
        student = Student.query.get(m.student_id)
        exam = Examination.query.get(m.exam_id)
        result.append({
            "id": m.id,
            "student_name": student.name if student else "Unknown",
            "exam_title": exam.exam_title if exam else "Unknown",
            "score": m.score,
            "grade": m.grade
        })
    return jsonify(result), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not Student.query.first():
            sample_student = Student(student_id="S001", name="Alice Smith", email="alice@example.com")
            sample_course = Course(course_code="CS101", course_name="Introduction to Programming")
            db.session.add_all([sample_student, sample_course])
            db.session.commit()
            
            sample_exam = Examination(exam_title="Midterm Exam", course_id=sample_course.id)
            db.session.add(sample_exam)
            db.session.commit()
            print("Database seeded with sample student and exam!")
            
    app.run(debug=True)