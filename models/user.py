from config import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Usergroups(db.Model):
    # Usergroups/Roles will be stored in this table
    __tablename__ = "usergroups"
    id = db.Column(db.SmallInteger, unique=True, primary_key=True)
    name = db.Column(db.String(10), unique=True, nullable=False)


class Users(db.Model, UserMixin):
    # Users information will be stored in this table
    __tablename__ = "users"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(45), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(
        db.DateTime, nullable=False, server_default=func.now())
    usergroup = db.Column(db.SmallInteger, db.ForeignKey(
        'usergroups.id'), nullable=False, server_default="1")
    usergroups = db.relationship(
        "Usergroups", backref=db.backref("usergroups", uselist=False))

    def get_id(self):
        return self.id

    def get_role(self):
        return Usergroups.query.filter_by(id=self.usergroup).first().name
