from extensions import *
from flask_less import lessc
from flask_limiter import Limiter
from flask import Flask, request
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
import logging
from logging.handlers import RotatingFileHandler
import os
from flask_wtf.csrf import CSRFProtect

current_dir = os.path.dirname(os.path.abspath(__file__))

sqlite_db_path = f"sqlite:///{os.path.join(current_dir, 'database.db')}"

db = SQLAlchemy()


def create_app():
    # Create an instance of the Flask class.
    app = Flask(__name__)

    # Set the SQL Alchemy Database URI.
    app.config["SQLALCHEMY_DATABASE_URI"] = sqlite_db_path

    # Signing cookies is a preventive measure against cookie tampering.
    # During the process of signing a cookie, the SECRET_KEY is used in
    # a way similar to how a "salt" would be used to muddle a password before hashing it.
    app.config["SECRET_KEY"] = "H34lth4dv1c3Gr0up333"

    cache = Cache(app, config={'CACHE_TYPE': 'simple'})

    # Create an instance of the CSRF Token.
    csrf = CSRFProtect(app)

    # Create an instance of the LoginManager class.
    login_manager = LoginManager()

    # Initialise helpers for use with this Flask instance.
    argon2.init_app(app)
    lessc(app)
    db.init_app(app)
    login_manager.init_app(app)

    # Define the route to direct users to when they encounter a page that requires login.
    login_manager.login_view = "login"

    # Define the error message to display when they encounter a page that requires login.
    login_manager.login_message = "Please login to access this page."

    # Create an instance of the Limiter class that will be used to handle route limiting.
    limiter = Limiter(
        app=app, key_func=lambda: request.remote_addr, storage_uri="memory://")

    # The API key for the OpenWeatherMap API
    openweathermap_api_key = "f8131773bee8069ac586fc7d2d701509"

    # Setup of the logging that will keep errors from being shown in the console.
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    app.logger.handlers.clear()
    file_handler = RotatingFileHandler(
        'error.log', maxBytes=1024 * 1024 * 10, backupCount=10)
    formatter = logging.Formatter(
        '\n%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return app, db, login_manager, limiter, openweathermap_api_key, logger, csrf, cache
