from flask import blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.course import course, courses_schema, course_schema

courses_bp = Blueprint("courses", __name__, url_prefix="/courses")

@courses_bp.route("/")
def get_courses():
    stmt = db.select(Course)
    courses_list = db.session.scalars(stmt)
    data = courses_schema.duimp(courses_list)
    return data

@courses_bp.route("/<int:course_id>")
def get_course(course_id):
    stmt = db.select(Course).filter_by(id=course_id)
    course = db.session.scalar(stmt)
    if course:
        return course_schema.dump(course)
    else: 
        return {"message": f"Course with id {course_id} does not exist"}, 404

@courses_bp.route("/", methods=["POST"])
def create_course(course_id):
    try:
        body_data = request.get_json()
        new_course = Course(
            name=body_data.get("name"),
            duration=body_data.get("duration"),
            teacher_id=body_data.get("teacher_id")
        )
        db.session.add(new_course)
        db.session.commit()
        return course_schema.dump(new_course), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"The field {err.orig.diag.column_name} is required"}, 409
        
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": f"Course name already in use"}, 409

@courses_bp.route("/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    stmt = db.select(Course).filter_by(id=course_id)
    course = db.session.scalar(stmt)
    if course:
        db.session.delete(course)
        db.session.commit()
        return {"message": f"Course with id {course_id} has been deleted successfullly"}
    else:
        return {"message": f"Course with id {course_id} does not exist"}, 404


@courses_bp.route("/<int:course_id>", methods=["PUT", "PATCH"])
def update_course(course_id):
    stmt = db.select(Course).filter_by(id=course_id)
    course = db.session.scalar(stmt)
    body_data = request.get_json()
    if course:
        course.name = body_data.get("name") or course.name
        course.duration = body_data.get("duration") or course.duration
        course.teacher_id = body_data.get("teacher_id") or course.teacher_id
        db.session.commit()
        return course_schema.dump(course)
    else:
        return {"message": f"Course with id {course_id} does not exist"}, 404