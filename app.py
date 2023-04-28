import os
import logging
from logging.handlers import RotatingFileHandler
from random import randrange
import secrets

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import or_

from database import configure_database, db_session, db
from models import Plant
from plant_info import get_plant_info
from dotenv import load_dotenv

# Initiate the Flask app
app = Flask(__name__)

# Load environment variables from a .env file
load_dotenv()

# Configure the database
configure_database(app)
migrate = Migrate(app, db)

# Import db_session after configure_database
from database import db_session

# Set the CSRF secret key
app.config['SECRET_KEY'] = secrets.token_hex(16)
csrf = CSRFProtect(app)

# Set the logging level to "DEBUG"
app.logger.setLevel(logging.DEBUG)

# Add a rotating file handler that writes messages to a log file
log_file = 'app.log'
file_handler = RotatingFileHandler(
    log_file, maxBytes=1024 * 1024, backupCount=5)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/')
def home():
    plants = Plant.query.all()
    if plants:
        random_plant = plants[randrange(len(plants))]
    else:
        random_plant = None
    return render_template('home.html', plants=plants, random_plant=random_plant)


@app.route('/plants')
def list_plants():
    plants = Plant.query.all()
    return render_template('list_plants.html', plants=plants)


@app.route('/search', methods=['GET'])
def search_plant():
    query = request.args.get('query')
    if query:
        # Search the database for a plant that matches the query
        plant = db.session.query(Plant).filter(
            or_(Plant.common_name.ilike(f'%{query}%'), Plant.scientific_name.ilike(f'%{query}%'))).first()
        return render_template('plant_info.html', plant_info=plant, query=query)
    else:
        # If there is no query parameter, redirect to the home page
        return redirect(url_for('home'))

@app.route('/plant_information/<int:plant_id>')
def plant_information(plant_id):
    # Get the plant information from the database
    plant = db_session.query(Plant).filter(Plant.id == plant_id).first()

    # Get additional plant information from the Trefle API
    plant_info = get_plant_info(plant.trefle_id)

    return render_template('plant_information.html', plant=plant, plant_info=plant_info)


@app.route('/add_to_database/<plant_name>', methods=['GET', 'POST'])
def add_to_database(plant_name):
    # Query the Trefle API for the plant data
    plant_data = query_trefle_api(plant_name)

    # If the user submits the form, add the plant to the database and redirect to the plant information page
    if request.method == 'POST':
        # Add the plant to the database
        add_plant_to_database(plant_data)

        # Redirect the user to the plant information page
        return redirect(url_for('plant_information', plant_id=plant_data['id']))

    # If the user has not submitted the form yet, display the plant data to the user for confirmation
    else:
        return render_template('add_to_database.html', plant_data=plant_data)
