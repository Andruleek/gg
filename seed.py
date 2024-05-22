from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Group, Student, Teacher, Subject, Grade
import random


# Initialize Faker and SQLAlchemy
faker = Faker()
engine = create_engine('sqlite:///university.db')
Session = sessionmaker(bind=engine)
session = Session()

# Create all tables
Base.metadata.create_all(engine)

# Generate Groups
groups = [Group(name=f"Group {i+1}") for i in range(3)]
session.add_all(groups)
session.commit()

# Generate Teachers
teachers = [Teacher(name=faker.name()) for _ in range(5)]
session.add_all(teachers)
session.commit()

# Generate Subjects
subjects = [Subject(name=faker.word().capitalize(), teacher=random.choice(teachers)) for _ in range(8)]
session.add_all(subjects)
session.commit()

# Generate Students
students = [Student(name=faker.name(), group=random.choice(groups)) for _ in range(50)]
session.add_all(students)
session.commit()

# Assign Subjects to Students
for student in students:
    student.subjects = random.sample(subjects, k=random.randint(3, 5))
session.commit()

# Generate Grades
grades = []
for student in students:
    for subject in student.subjects:
        for _ in range(random.randint(15, 20)):
            grade = Grade(student=student, subject=subject, grade=random.randint(1, 100))
            grades.append(grade)

session.add_all(grades)
session.commit()

# Close session
session.close()
