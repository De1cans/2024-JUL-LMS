from Flask import Blueprint

from init import db
from models.student import Student, student_schema, students_schema

students_db = Blueprint("students", __name__, url_prefix="/students")

@students_bp.route("/")
def get_students():
    db.select(Student)
    students_list = db.session.scalars(stmt)
    data = students_schema.dump(students_list)
    return data

@students_bp.route("/<int:student_id>")
def get_student(student_id):
    stmt = db.select(Student).filter_by(id=student_id)
    student = db.session.scalar(stmt)
    if student:
        data = student_schema.dump(student)
        return data
    else:
        return {"message": f"Student with id {student_id} does not exist"}, 404