import os
import logging
from logging.handlers import RotatingFileHandler
from random import randrange
import secrets

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import or_

from database import configure_database, db
from models import Plant
from plant_info import get_plant_info
from dotenv import load_dotenv
from forms import SearchForm

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


@app.route('/search', methods=['GET', 'POST'])
def search_plant():
    query = request.args.get('query')
    if query:
        print("Search query received:", query)  # Debugging print statement
        # Search the database for plants that match the query
        plants = db_session.query(Plant).filter(
            or_(Plant.common_name.ilike(f'%{query}%'), Plant.scientific_name.ilike(f'%{query}%'))).all()
        if plants:
            print("Plants found in the database:", plants)  # Debugging print statement
            # If the plant is found in the database, show the plant info
            return render_template('plant_info.html', plants=plants, query=query)
        else:
            print("No plants found in the database, fetching data from the Trefle API")  # Debugging print statement
            # If the plant is not found in the database, fetch the data from the Trefle API
            plant_info = plant_info.get_plant_info(query.strip())
            if plant_info:
                print("Plant data found in the Trefle API:", plant_info)  # Debugging print statement
                # If the plant data is found in the Trefle API, show the search results
                return render_template('search_results.html', name=query, result=plant_info)
            else:
                print("No plant data found in the Trefle API")  # Debugging print statement
                # If the plant data is not found in the Trefle API, show a message to the user
                flash(f'No plant named "{query}" found.')
    else:
        print("No query parameter received")  # Debugging print statement

    # If there is no query parameter, redirect to the home page
    return redirect(url_for('home'))



@app.route('/search_results', methods=['POST'])
def search_results():
    form = SearchForm()
    if form.validate_on_submit():
        common_name = form.common_name.data
        plant = Plant.query.filter_by(common_name=common_name).first()
        if plant:
            return render_template('plant.html', plant=plant)
        else:
            flash('No plant found with that common name')
            return redirect(url_for('search_plant'))
    return render_template('search_plant.html', form=form)


@app.route('/plant_information/<int:plant_id>')
def plant_information(plant_id):
    # Get the plant information from the database
    plant = db_session.query(Plant).filter(Plant.id == plant_id).first()

    # Get additional plant information from the Trefle API
    plant_info = get_plant_info(plant.trefle_id)

    return render_template('plant_information.html', plant=plant, plant_info=plant_info)


# Define the route for adding a new plant
@app.route('/add_plant', methods=['GET', 'POST'])
def add_plant():
    form = SearchForm()
    if form.validate_on_submit():
        query = form.query.data
        return redirect(url_for('search_plant', query=query))
    return render_template('add_plant.html', form=form)


# Define the route for adding the new plant to the database
@app.route('/add_to_database', methods=['POST'])
def add_to_database():
    # Retrieve the data for the new plant from the form
    common_name = request.form['common_name']
    scientific_name = request.form['scientific_name']
    sunlight_care = request.form['sunlight_care']
    water_care = request.form['water_care']
    temperature_care = request.form['temperature_care']
    humidity_care = request.form['humidity_care']
    growing_tips = request.form['growing_tips']
    propagation_tips = request.form['propagation_tips']
    common_pests = request.form['common_pests']
    image_url = request.form['image_url']
    family = request.form['family']
    genus = request.form['genus']
    year = request.form['year']
    edible = request.form['edible']
    edible_part = request.form['edible_part']
    edible_notes = request.form['edible_notes']
    medicinal = request.form['medicinal']
    medicinal_notes = request.form['medicinal_notes']
    toxicity = request.form['toxicity']
    synonyms = request.form['synonyms']
    native_status = request.form['native_status']
    conservation_status = request.form['conservation_status']

    # Create a new Plant object with the retrieved data
    new_plant = Plant(
        common_name=common_name,
        scientific_name=scientific_name,
        sunlight_care=sunlight_care,
        water_care=water_care,
        temperature_care=temperature_care,
        humidity_care=humidity_care,
        growing_tips=growing_tips,
        propagation_tips=propagation_tips,
        common_pests=common_pests,
        image_url=image_url,
        family=family,
        genus=genus,
        year=year,
        edible=edible,
        edible_part=edible_part,
        edible_notes=edible_notes,
        medicinal=medicinal,
        medicinal_notes=medicinal_notes,
        toxicity=toxicity,
        synonyms=synonyms,
        native_status=native_status,
        conservation_status=conservation_status
    )

    print("New plant object before committing:", new_plant)

    # Add the new plant to the database and commit the changes
    db_session.add(new_plant)
    db_session.commit()

    print("New plant object after committing:", new_plant)

    # Redirect to the home page
    return redirect(url_for('home'))
