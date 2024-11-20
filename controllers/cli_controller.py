from flask import Blueprint

from init import db
from models.student import Student
from models.teacher import Teacher
from models.course import Course

db_commands = Blueprint("db", __name__)


@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created")


@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped")


@db_commands.cli.command("seed")
def seed_tables():

    students = [
        Student(
            name="Student 1",
            email="student1@email.com",
            address="Sydney"
        ),
        Student(
            name="Student 2",
            email="student2@email.com",
            address="Melbourne"
        )
    ]

    db.session.add_all(students)

    teachers = [
        Teacher(
            name="Teacher 1",
            department="Engineering",
            address="Sydney"
        ),
        Teacher(
            name="Teacher 2",
            department="Management",
            address="Melbourne"
        )
    ]

    db.session.add_all(teachers)

    courses = [
        Course(
            name="Course 1",
            duration=1,
            teacher_id=teachers[0].id
        ),
        Course(
            name="Course 2",
            duration=2,
            teacher_id=teachers[0].id
        ),
        Course(
            name="Course 3",
            duration=2,
            teacher_id=teachers[1].id
        ),
        Course(
            name="Course 4",
            duration=3,
            teacher_id=teachers[1].id
        )
    ]

    db.sesstion.add_all(courses)

    db.session.commit()

    print("Tables seeded")