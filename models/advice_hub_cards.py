from config import db
from flask_login import UserMixin


class AdviceHubCards(db.Model, UserMixin):
    # Advice hub cards will be stored in this table
    __tablename__ = "advice_hub_cards"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    company = db.Column(db.String, nullable=False)
    route = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)
