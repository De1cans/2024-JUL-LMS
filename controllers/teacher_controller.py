from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.teacher import Teacher, teachers_schema, teacher_schema

teachers_bp = Blueprint("teachers", __name__, url_prefix="/teachers")

# Create - /teachers - POST
# Read all - /teachers - GET
# Read one - /teachers/id - GET
# Update - /teachers/id - PUT, PATCH
# Delete - /teachers/id - DELETE


# Read all - /teachers - GET
@teachers_bp.route("/")
def get_teachers():
    department = request.args.get("department")
    if department:
        stmt = db.select(Teacher).filter_by(department=department).order_by(Teacher.id)
    else:
        stmt = db.select(Teacher).order_by(Teacher.id)
    teachers_list = db.session.scalars(stmt)
    data = teachers_schema.dump(teachers_list)
    return data


# Read one - /teachers/id - GET
@teachers_bp.route("/<int:teacher_id>")
def get_teacher(teacher_id):
    stmt = db.select(Teacher).filter_by(id=teacher_id)
    teacher = db.session.scalar(stmt)
    if teacher:
        return teacher_schema.dump(teacher)
    else:
        return {"message": f"Teacher with id {teacher_id} does not exist"}, 404


# Create - /teachers - POST
@teachers_bp.route("/", methods=["POST"])
def create_teacher():
    try:
        body_data = request.get_json()
        new_teacher = Teacher(
            name=body_data.get("name"),
            department=body_data.get("department"),
            address=body_data.get("address"),
        )
        db.session.add(new_teacher)
        db.session.commit()

        return teacher_schema.dump(new_teacher), 201
    
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"The '{err.orig.diag.column_name}' is required"}, 409


# Delete - /teachers/id - DELETE
@teachers_bp.route("/<int:teacher_id>", methods=["DELETE"])
def delete_teacher(teacher_id):
    stmt = db.select(Teacher).filter_by(id=teacher_id)
    teacher = db.session.scalar(stmt)
    if teacher:
        db.session.delete(teacher)
        db.session.commit()
        return {"message": f"Teacher '{teacher.name}' deleted successfuly"}
    else:
        return {"message": f"Teacher with id {teacher_id} does not exist"}, 404


# Update - /teachers/id - PUT, PATCH
@teachers_bp.route("/<int:teacher_id>", methods=["PUT", "PATCH"])
def update_teacher(teacher_id):
    # find the teacher with that id from the db
    stmt = db.select(Teacher).filter_by(id=teacher_id)
    teacher = db.session.scalar(stmt)
    # get the data to be updated - receive from request body
    body_data = request.get_json()
    # if teacher exists
    if teacher:
        # update the attributes
        teacher.name = body_data.get("name") or teacher.name
        teacher.address = body_data.get("address") or teacher.address
        teacher.department = body_data.get("department") or teacher.department
        # commit
        db.session.commit()
        # return a response
        return teacher_schema.dump(teacher)
    # else
    else:
        # return an error response
        return {"message": f"Teacher with id {teacher_id} does not exist"}, 404