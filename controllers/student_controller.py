from Flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

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

@student_bp.route("/", methods=["POST"])
def create_student():
    try:
        body_data = request.get_json()
        new_student = Student(
            name=body_data.get("name"),
            email=body_data.get("email"),
            address=body_data.get("address")
        )
        db.session.add(new_student)
        db.session.commit()
        return student_schema.dump(new_student), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            # not null violation
            return {"message": f"The field {err.orig.diag.column_name} is required"}, 409
        
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            # unique constriant violation
            return {"message": "Email address already in use"}, 409

@student_bp.route("/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    stmt = db.select(Student).filter_by(id=student_id)
    student = db.session.scalar(stmt)
    if student:
        db.session.delete(student)
        db.session.commit()
        return {"message": f"Student with id {student_id} has been deleted successfully"}
    else: 
        return {"message": f"Student with id {student_id} does not exist"}, 404

@student_bp.route("/<int:student_id", methods=["PUT", "PATCH"])
def update_student(student_id):
    stmt = db.select(Student).filter_by(id=student_id)
    student = db.session.scalar(stmt)
    body_data = request.get_json()
    if student:
        student_name = body_data.get("name") or student.name
        student_email = body_data.get("email") or student.email
        student_address = body_data.get("address") or student.address
        db.session.commit()
        return student_schema.dump(student)
    else:
        return {"message": f"Student with id {student_id} does not exist"}, 404