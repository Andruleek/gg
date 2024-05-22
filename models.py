from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()

# Association table for many-to-many relationship between Students and Subjects
student_subject_association = Table(
    'student_subject', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('subject_id', Integer, ForeignKey('subjects.id'))
)

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    group_id = Column(Integer, ForeignKey('groups.id'))
    group = relationship("Group", back_populates="students")
    subjects = relationship("Subject", secondary=student_subject_association, back_populates="students")

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    teacher = relationship("Teacher", back_populates="subjects")
    students = relationship("Student", secondary=student_subject_association, back_populates="subjects")

class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    grade = Column(Integer)
    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")

Group.students = relationship("Student", order_by=Student.id, back_populates="group")
Teacher.subjects = relationship("Subject", order_by=Subject.id, back_populates="teacher")
Student.grades = relationship("Grade", order_by=Grade.id, back_populates="student")
Subject.grades = relationship("Grade", order_by=Grade.id, back_populates="subject")
