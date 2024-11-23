from marshmallow import fields

from init import db, ma


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    duration = db.Column(db.Float)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))

    teacher = db.relationship("Teacher", back_populates="courses")

    enrolment = db.relationship("Enrolment", back_populates="course", cascase="all, delete")


# id: 1,
# name: "Course 1",
# duration: 1,
# teacher_id: 1,
# teacher: {
#   id: 1,
#   name: "Teacher 1",
#   department: "Engineering"
# }


class CourseSchema(ma.Schema):
    ordered=True
    teacher = fields.Nested("TeacherSchema", only=["name", "department"])
    enrolments = fields.List(fields.Nested("EnrolmentSchema", exclude=["course"]))
    class Meta:
        fields = ("id", "name", "duration", "teacher_id", "teacher", "enrolments")


course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)