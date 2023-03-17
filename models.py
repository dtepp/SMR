from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin
 
db = SQLAlchemy()
 
    # CONFIGURE TABLES
class User(UserMixin, db.Model):
        __tablename__ = "users"
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(250), unique=True)
        password = db.Column(db.String(250))
        name = db.Column(db.String(250))
        majors = relationship("SchoolMajor", back_populates="author")
        levels = relationship("SchoolLevel", back_populates="level_author")


class SchoolMajor(db.Model):
        __tablename__ = "schoolmajors"
        id = db.Column(db.Integer, primary_key=True)
        author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
        author = relationship("User", back_populates="majors")
        majorName = db.Column(db.String(250),  nullable=False)
        school = db.Column(db.String(250), nullable=False)
        applyReq = db.Column(db.Text, nullable=False)
        langReq = db.Column(db.Text, nullable=False)
        Fee = db.Column(db.Text, nullable=True)
        course = db.Column(db.Text, nullable=False)
        cluster = db.Column(db.String(250), nullable=True)
        label = db.Column(db.String(250), nullable=True)
        date = db.Column(db.String(250), nullable=False)
        IELTS = db.Column(db.String(10),nullable=True)
        TOEFL = db.Column(db.String(10),nullable=True)


class SchoolLevel(db.Model):
        __tablename__ = "schoollevels"
        id = db.Column(db.Integer, primary_key=True)
        author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
        level_author = relationship("User", back_populates="levels")
        countryName=db.Column(db.Text,nullable=True )
        schoolname=db.Column(db.Text,nullable=False )
        isApply=db.Column(db.Boolean,nullable=True )
        isAddOn=db.Column(db.Boolean,nullable=True )
        schoolscore=db.Column(db.Text, nullable=True)
        addscore=db.Column(db.Text, nullable=True)
        date = db.Column(db.String(250), nullable=False)