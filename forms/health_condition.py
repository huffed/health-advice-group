from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import InputRequired, ValidationError
from models.user import Users
from extensions import argon2
from config import db
from sqlalchemy import text


class HealthConditionForm(FlaskForm):
    condition = SelectField(
        validators=[InputRequired()], choices=["Select...", "Common cold", "Influenza", "COVID-19", "Chest cold", "Asthma", "Pneumonia", "Conjunctivitis", "Sinus infection", "Strep throat", "Stomach bug"])

    submit = SubmitField(render_kw={"value": "+"})

    def validate_condition(self, condition):
        if condition.data == "Select...":
            raise ValidationError("Invalid condition")
