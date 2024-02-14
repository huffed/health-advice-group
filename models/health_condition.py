from config import db
from flask_login import UserMixin


class HealthConditions(db.Model, UserMixin):
    # Health Conditions will be stored in this table
    __tablename__ = "health_conditions"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    users = db.relationship(
        "Users", backref=db.backref("users", uselist=False))
