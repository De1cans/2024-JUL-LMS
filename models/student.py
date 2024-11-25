from marshmallow import fields

from init import db, ma

class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    address = db.Column(db.String(100))

    enrolments = db.relationship("Enrolment", back_populates="student", cascade="all, delete")

class StudentSchema(ma.Schema):
    enrolments = fields.List(fields.Nested("EnrolmentSchema"), exclude=["student"])
    class Meta:
        fields = ("id", "name", "email", "address", "enrolments")

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)