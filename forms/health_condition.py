from flask import g
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import InputRequired, ValidationError
from config import db
from sqlalchemy import text


class HealthConditionForm(FlaskForm):
    condition = SelectField(
        validators=[InputRequired()], choices=['Select...', 'Common cold', 'Influenza', 'COVID-19', 'Chest cold', 'Asthma', 'Pneumonia', 'Conjunctivitis', 'Sinus infection', 'Strep throat', 'Stomach bug'])

    submit = SubmitField(render_kw={'value': '+'})

    def validate_condition(self, condition):
        if condition.data == 'Select...':
            raise ValidationError('Invalid condition')

        query = text(
            'SELECT name FROM health_conditions WHERE name = :name AND uid = :uid'
        )

        health_condition_exists = db.session.execute(query, {
            'name': condition.data,
            'uid': g.user.id
        }).fetchone()

        if health_condition_exists:
            raise ValidationError('Condition already registered')
