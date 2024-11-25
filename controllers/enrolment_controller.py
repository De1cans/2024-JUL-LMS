from flask import Blueprint, request

from init import db
from models.enrolment import Enrolment, enrolments_schema, enrolment_schema

enrolments_bp = Blueprint("enrolments", __name__, url_prefix="/enrolments")

# Read all
@enrolments_bp.route("/")
def get_enrolments():
    student_id = request.args.get("student_id")
    if student_id:
        stmt = db.select(Enrolment).filter_by(student_id=student_id)
    else:
        stmt = db.select(Enrolment)
    enrolments_list = db.session.scalars(stmt)
    return enrolments_schema.dump(enrolments_list)


# Read one
@enrolments_bp.route("/<int:enrolment_id>")
def get_enrolment(enrolment_id):
    stmt = db.select(Enrolment).filter_by(id=enrolment_id)
    enrolment = db.session.scalar(stmt)
    if enrolment:
        return enrolment_schema.dump(enrolment)
    else:
        return {"message": f"Enrolment with id {enrolment_id} doesn't exist"}, 404