
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
import base64,sqlalchemy 
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(255),unique =True,nullable=False)
    password = db.Column(db.String(255),nullable = False)
    
    def __repr__(self):
        return f'<User {self.email}>'