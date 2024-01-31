from flask import render_template, url_for, redirect, request
from sqlalchemy import text
from flask_login import login_user, login_required, current_user, logout_user
from config import create_app
from extensions import argon2

from models.user import Usergroups, Users

app, database, login_manager, limiter, logger, csrf = create_app()

with app.app_context():
    database.create_all()


@login_manager.user_loader
def load_user(user_id):
    query = text(
        "SELECT id, username, password FROM users WHERE id = :user_id"
    )
    result = database.session.execute(query, {"user_id": user_id}).fetchone()

    if result:
        id, username, password = result
        return Users(id=id, username=username, password=password)


@app.context_processor
def context_processor():
    return dict(user=current_user, active_page=request.path)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")
