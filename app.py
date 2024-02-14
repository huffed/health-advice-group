# GENERAL IMPORTS
from forms.user import RegisterForm, LoginForm
from models.user import Usergroups, Users
from flask import render_template, url_for, redirect, request
from sqlalchemy import text
from flask_login import login_user, login_required, current_user, logout_user
from config import create_app
from extensions import argon2
import datetime
import requests
import json
import ipapi

# MODELS

# FORMS

# Use the create_app function from the config to generate the values
# for all the constructor type variables.
app, database, login_manager, limiter, openweathermap_api_key, logger, csrf = create_app()

# Create database tables on startup if they haven't been created already.
with app.app_context():
    database.create_all()


@login_manager.user_loader
def load_user(user_id):
    # Defining the process for logging a user in.

    # Providing the SQL statement that will be used to
    # get the user that has the id provided in the parameters.
    query = text(
        'SELECT id, username, password FROM users WHERE id = :user_id'
    )
    # Get the user that has the id provided in the parameters.
    result = database.session.execute(query, {'user_id': user_id}).fetchone()

    if result:  # If the user exists.
        id, username, password = result  # Expanding the result
        return Users(id=id, username=username, password=password)


@app.context_processor
def context_processor():
    # These functions run before rendering a template.
    return dict(user=current_user, active_page=request.path)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # This is the route for processing requests on the /register route

    # Providing the form that will be used on the page
    form = RegisterForm()

    # This defines the processes that will happen when the form is submitted
    if form.validate_on_submit():

        # Hashing the password that is provided by the form using the Argon2 algorithm
        hashed_password = argon2.generate_password_hash(form.password.data)

        # Providing the SQL statement that will be used to insert the user into the database
        query = text(
            'INSERT INTO users (username, email, password) VALUES (:username, :email, :password)'
        )
        try:
            # Attempts to insert the user into the database
            database.session.execute(
                query, {'username': form.username.data, 'email': form.email.data, 'password': hashed_password})
            database.session.commit()

            return redirect(url_for('login'))
        except Exception as error:
            # If there are any problems inserting the user into the database
            # The database committing session will rollback for security and raise the error
            database.session.rollback()
            raise error

    # Load the register-login template and providing the form and
    # form_type variables for the template to use
    return render_template('register-login.html', form=form, form_type=request.path.strip('/'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    # This is the route for processing requests on the /login route

    # Providing the form that will be used on the page
    form = LoginForm()

    # This defines the processes that will happen when the form is submitted
    if form.validate_on_submit():

        # Providing the SQL statement that will be used to search for the user in the database
        query = text(
            'SELECT * FROM users WHERE username = :username'
        )

        # Attempts to get the user from the database using their username
        user = database.session.execute(
            query, {'username': form.username.data}).fetchone()

        # If the user exists and the password matches the hash
        if user and argon2.check_password_hash(user.password, form.password.data):

            # Login the user using the login_user function providing the User class that is needed
            login_user(Users(**user._mapping), remember=form.remember.data)

            # If they have accessed the page via attempting to access a page that requires a login
            try:
                return redirect(url_for(request.args['next'].strip('/')))
            # If they have accessed the page directly
            except:
                return redirect(url_for('index'))
        else:
            return render_template('register-login.html', form=form, form_type=request.path.strip('/'))

    return render_template('register-login.html', form=form, form_type=request.path.strip('/'))


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    request.remote_addr = "51.191.63.28"
    # Create location variable containing the country, city, longitude, latitude etc of user
    # This uses the ip-api.com api to get this information
    location = requests.get(
        f'http://ip-api.com/json/{request.remote_addr}').json()

    # If location cannot be found with the IP from the request
    if location['status'] == 'fail':
        'Location not found.'
    else:
        # If the location can be found with the IP from the request
        # Get the weather and air pollutioninformation of the location
        # based off the longitude and latitude from the location dictionary
        weather = json.loads(requests.get(
            url='http://api.openweathermap.org/data/2.5/weather',
            params={
                'lat': str(location["lat"]),
                'lon': str(location["lon"]),
                'appid': openweathermap_api_key
            }).text)

        air_pollution = requests.get(
            url='http://api.openweathermap.org/data/2.5/air_pollution',
            params={
                'lat': str(location["lat"]),
                'lon': str(location["lon"]),
                'appid': openweathermap_api_key
            }).json()

    return render_template('dashboard/index.html', location=location, weather=weather, air_pollution=air_pollution)


@app.route('/dashboard/advice', methods=['GET', 'POST'])
def advice_hub():
    pass


@app.route('/dashboard/map', methods=['GET', 'POST'])
def pollution_map():
    pass


@app.route('/location/<location_id>')
def location(location_id):
    # Make a request to the OpenAQ API to get the air quality information for the specified location
    response = requests.get(
        f'https://api.openaq.org/v1/measurements?location_id={location_id}')

    # Parse the JSON response
    measurements = response.json()['results']

    # Render the template with the air quality information
    return render_template('location.html', measurements=measurements)
