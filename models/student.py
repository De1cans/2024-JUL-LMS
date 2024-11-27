from marshmallow import fields
from marshmallow.validate import OneOf

from init import db, ma

VALID_ADDRESSES = ("Sydney", "Melbourne", "Brisbane", "Perth")

class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    address = db.Column(db.String(100))

    enrolments = db.relationship("Enrolment", back_populates="student", cascade="all, delete")

class StudentSchema(ma.Schema):

    address = fields.String(validate=Oneof(VALID_ADDRESSES))

    enrolments = fields.List(fields.Nested("EnrolmentSchema"), exclude=["student"])
    class Meta:
        fields = ("id", "name", "email", "address", "enrolments")

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)