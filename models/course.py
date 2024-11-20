from marshmallow import fields

from init import db, ma

class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    duration = db.Column(db.Float)
    teacher_id = db.Columnn(db.Integer, db.ForeignKey("teachers.id"))

    teacher = db.relationship("Teacher", back_populates="courses")

class CourseSchema(ma.Schema):
    ordered=True
    teacher = fields.Nested("TeacherSchema", only=["name", "department"])
    class Meta:
        fields = ("id", "name", "duration", "teacher_id", "teacher")

course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)