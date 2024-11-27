from marshmallow import fields
from marshmallow.validate import Length, And, Regexp

from init import db, ma


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    duration = db.Column(db.Float)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))

    teacher = db.relationship("Teacher", back_populates="courses")

    enrolments = db.relationship("Enrolment", back_populates="course", cascade="all, delete")

# id: 1,
# name: "Course 1",
# duration: 1,
# teacher_id: 1,
# teacher: {
#   id: 1,
#   name: "Teacher 1",
#   department: "Engineering"
# },
# enrolments: [
# {
#   id: 1,
#   enrolment_date: "2022-10-20",
#   student_id: 1,
#   course_id: 2,
# },
# {
#   id: 2,
#   enrolment_date: "2024-08-20",
#   student_id: 2,
#   course_id: 1,
# }
# ]


class CourseSchema(ma.Schema):
    name = fields.String(required=True, validate=And(
        Length(min=2, error="name must be at least 2 characters long"),
        Regexp('^[A-Za-z0-9][A-Za-z0-9 ]*$+', error="Only letters, numbers and spaces are allowed")
    ))

    ordered=True
    teacher = fields.Nested("TeacherSchema", only=["name", "department"])
    enrolments = fields.List(fields.Nested("EnrolmentSchema", exclude=["course"]))
    class Meta:
        fields = ("id", "name", "duration", "teacher_id", "teacher", "enrolments")


course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)