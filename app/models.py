from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from passlib.hash import bcrypt_sha256
from flask_bcrypt import Bcrypt
from flask import redirect, url_for
from datetime import datetime

bcrypt = Bcrypt()

@login_manager.user_loader
def load_user(user_id):
    from app.models import Roommate, Admin, FamilyMember
    roommate = Roommate.query.get(user_id)
    if roommate:
        return roommate
    familyMember = FamilyMember.query.get(user_id)
    if familyMember:
        return familyMember
    admin = Admin.query.get(user_id)
    if admin:
        return admin
    return None

class Roommate(db.Model, UserMixin):
    __tablename__ = 'roommate'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False) 
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='roommate')
    RoommateName = db.Column(db.String(50), unique=False, nullable=False)
    contacted = db.Column(db.Boolean, nullable=True, default=False)
    registeredAt = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    def __init__(self, email, password, contacted, RoommateName, registeredAt, role='roommate'):
        self.email = email
        self.RoommateName = RoommateName
        self.password = password
        self.role = role
        self.contacted = contacted
        self.registeredAt = registeredAt

# class Teacher(db.Model, UserMixin):
#     __tablename__ = 'teacher'
#     id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
#     email = db.Column(db.String(50), unique=True, nullable=False) 
#     password = db.Column(db.String(100), nullable=False)
#     TeacherID = db.Column(db.String(100), unique=False, nullable=False)
#     role = db.Column(db.String(10), nullable=False, default='teacher')
#     teacherName = db.Column(db.String(50), unique=False, nullable=False)
#     teacherSubject = db.Column(db.String(50), unique=False, nullable=False)
#     TeacherClass = db.Column(db.String(250), unique=False, nullable=False)
#     isOnline = db.Column(db.Boolean, nullable=True, default=False)
#     contacted = db.Column(db.Boolean, nullable=True, default=False)
#     school = db.Column(db.String(100), nullable=True)
#     registeredAt = db.Column(db.DateTime, default=datetime.now(), nullable=False)

#     def __init__(self, id, email, password, TeacherID, contacted, school, teacherName, TeacherClass, teacherSubject, isOnline, registeredAt, role='parent'):
#         self.id = id
#         self.email = email
#         self.teacherName = teacherName
#         self.teacherSubject = teacherSubject
#         self.password = password
#         self.TeacherID = TeacherID.capitalize()
#         self.TeacherClass = TeacherClass
#         self.role = role
#         self.contacted = contacted
#         self.isOnline = isOnline
#         self.school = school
#         self.registeredAt = registeredAt

class FamilyMember(db.Model, UserMixin):
    __tablename__ = 'familymember'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False) 
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='familymember')
    FamilyMemberName = db.Column(db.String(50), unique=False, nullable=False)
    contacted = db.Column(db.Boolean, nullable=True, default=False)
    registeredAt = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    def __init__(self, email, password, contacted, FamilyMemberName, registeredAt, role='familymember'):
        self.email = email
        self.FamilyMemberName = FamilyMemberName
        self.password = password
        self.role = role
        self.contacted = contacted
        self.registeredAt = registeredAt

class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='admin')

    def __init__(self, id, name, username, password, role='admin'):
        self.id = id
        self.name = name
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.role = role

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def create_admin():
        if not Admin.query.filter_by(username='admin').first():
            default_admin = Admin(
                id=1,
                name='Admin',
                username='admin',
                password='admin1234'
            )
            db.session.add(default_admin)
            db.session.commit()