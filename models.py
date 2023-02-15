"""Models authintication project"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db=SQLAlchemy()
bcrypt=Bcrypt()

def connect_db(app):

    db.app=app
    db.init_app(app)

class User(db.Model):
    """user for site"""
    __tablename__="users"
    
    username=db.Column(db.String(20),primary_key=True,unique=True,nullable=False) #no longer than 20 char
    password=db.Column(db.Text,nullable=False)
    email=db.Column(db.String(50),unique=True) #no longer than 50 char
    firstname=db.Column(db.String(30),nullable=False) #no longer than 30 char
    lastname=db.Column(db.String(30),nullable=False) #no longer then 3o char

    feedback = db.relationship("Feedback", backref="user", cascade="all,delete")

    @classmethod
    def register(cls,username,password,email,firstname,lastname):
        """Register a user, hashing their password."""

        hashed=bcrypt.generate_password_hash(password)
        hashed_utf8=hashed.decode("utf8")
        return cls(
            
            username=username,
            password=hashed_utf8,
            email=email,
            firstname=firstname,
            lastname=lastname,
        )
        
       
    @classmethod
    def authenticate(cls,username,password):
        """validate user and log in if valid else return False"""

        u=User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password,password):
            #returns user instance
            return u
        else:
            return False

class Feedback(db.Model):

    """feedback posts for site"""
    __tablename__="feedback"

    id=db.Column(db.Integer,primary_key=True,unique=True,autoincrement=True)
    title=db.Column(db.String(50),nullable=False)
    content=db.Column(db.Text,nullable=False)
    username=db.Column(db.String(20),db.ForeignKey('users.username'),nullable=False)

