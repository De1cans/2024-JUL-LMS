from flask import blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.techer import teacher, teachers_schema, teacher_schema

teachers_bp = Blueprint("teachers", __name__, url_prefix=("/teachers"))

@teachers_bp.route("/")
def get_teachers():
    department = request.args.get("department")
    if department:
        stmt = db.select(Teacher).filter_by(department=department)
    else:
        stmt = db.select(Teacher)
    teachers_list = db.session.scalars(stmt)
    data = teachers_schema.dump(teachers_list)
    return data


@teachers_bp.route("/<int:teacher_id>")
def get_teacher(teacher_id):
    stmt = db.select(Teacher).filter_by(id=teacher_id)
    teacher = db.session.scalar(stmt)
    if teacher:
        return teacher_schema.dump(teacher)
    else:
        return {"message": f"Teacher with id {teacher_id} does not exist"}, 404

@teachers_bp.route("/", methods=["POST"])
def create_teacher():
    try:
        body_data = request.get_json()
        new_teacher = Teacher(
            name=body_data.get("name"),
            department=body_data.get("department"),
            address=body_data.get("address")
        )
        db.session.add(new_teacher)
        db.session.commit()
        return teacher_schema.dump(new_teacher), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"The field {err.orig.diag.column_name} is required"}, 409

@teachers_bp.route("/<int:teacher_id>", methods=["DELETE"])
def delete_teacher(teacher_id):
    stmt = db.select(Teacher).fitler_by(id=teacher_id)
    teacher = db.session.scalar(stmt)
    if teacher:
        db.session.delete(teacher)
        db.session.commit()
        return {"message": f"Teacher with id {teacher_id} has been deleted successfully"}
    else:
        return {"message": f"Teacher with id {teacher_id} does not exist"}

@teacher_bp.route("/<int:teacher_id>", methods=["PUT", "PATCH"])
def update_teacher(teacher_id):
    stmt = db.select(Teacher).filter_by(id=teacher_id)
    teacher = db.session.scalar(stmt)
    body_data = request.get_json()
    if teacher:
        teacher.name = body_data.get("name") or teacher.name
        teacher.department = body_data.get("department") or teacher.department
        teacher.address = body_data.get("address") or teacher.address
        db.session.commit()
        return teacher_schema.dump(teacher)
    else:
        return {"message": f"Teacher with id {teacher_id} does not exist"}, 404