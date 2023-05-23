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

# Import db_session after configure_database
from database import db_session

# Initiate the Flask app
app = Flask(__name__)

# Load environment variables from a .env file
load_dotenv()

# Configure the database
configure_database(app)
migrate = Migrate(app, db)

# Set the CSRF secret key
app.config['SECRET_KEY'] = secrets.token_hex(16)
csrf = CSRFProtect(app)

# Set the logging level
app.logger.setLevel(logging.ERROR)

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


# @app.before_request
# def log_request_info():
#     app.logger.debug('Request headers: %s', request.headers)
#     app.logger.debug('Request body: %s', request.get_data())
#
#
@app.after_request
def log_response_info(response):
    app.logger.debug('Response headers: %s', response.headers)
    if not response.direct_passthrough:
        app.logger.debug('Response body: %s', response.get_data())
    else:
        app.logger.debug('Response is in direct passthrough mode')
    return response


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
    query = request.args.get('query') or request.form.get('query')
    get_detailed_info = request.form.get('get_detailed_info', False)
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
            print("No plants found in the database, fetching data from the Perenual API")  # Debugging print statement
            # If the plant is not found in the database, fetch the data from the Perenual API
            fetched_plant_info = get_plant_info(query.strip(), get_detailed_info)
            if fetched_plant_info:
                print("Plant data found in the Perenual API:", fetched_plant_info)  # Debugging print statement
                # If the plant data is found in the Perenual API, show the search results
                return render_template('search_results.html', plant=fetched_plant_info)
            else:
                print("No plant data found in the Perenual API")  # Debugging print statement
                # If the plant data is not found in the Perenual API, show a message to the user
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
            return render_template('plant_info.html', plant=plant)
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

    return render_template('plant_info.html', plant=plant, plant_info=plant_info)


# Define the route for adding a new plant
@app.route('/add_plant', methods=['GET', 'POST'])
def add_plant():
    form = SearchForm()
    if form.validate_on_submit():
        query = form.query.data
        return redirect(url_for('search_plant', query=query))
    return render_template('add_plant.html', form=form)


@app.route('/manual_entry')
def manual_entry():
    return render_template('manual_entry.html')


# Define the route for adding the new plant to the database
@app.route('/add_to_database', methods=['POST'])
def add_to_database():
    print("add_to_database route reached")  # Debugging print statement
    #  print(request.form.get('csrf_token'))

    app.logger.debug('Request headers: %s', request.headers)
    app.logger.debug('Request body: %s', request.get_data())
    print(request.form)

    # Retrieve the data for the new plant from the form
    common_name = request.form.get('common_name') or None
    scientific_name = request.form.get('scientific_name') or None
    sunlight_care = request.form.get('sunlight_care') or None
    water_care = request.form.get('water_care') or None
    temperature_care = request.form.get('temperature_care') or None
    humidity_care = request.form.get('humidity_care') or None
    growing_tips = request.form.get('growing_tips') or None
    propagation_tips = request.form.get('propagation_tips') or None
    common_pests = request.form.get('common_pests') or None
    image_url = request.form.get('image_url') or None
    family = request.form.get('family') or None
    genus = request.form.get('genus') or None
    year = request.form.get('year') or None
    edible = request.form.get('edible') or None
    edible_part = request.form.get('edible_part') or None
    edible_notes = request.form.get('edible_notes') or None
    medicinal = request.form.get('medicinal') or None
    medicinal_notes = request.form.get('medicinal_notes') or None
    toxicity = request.form.get('toxicity') or None
    synonyms = request.form.get('synonyms') or None
    native_status = request.form.get('native_status') or None
    conservation_status = request.form.get('conservation_status') or None

    print("Form data retrieved successfully")  # Debugging print statement

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

    print("New plant object created successfully")  # Debugging print statement
    print("New plant object before committing:", new_plant)

    # Add the new plant to the database and commit the changes
    db_session.add(new_plant)
    db_session.commit()

    print("New plant object after committing:", new_plant)

    # Redirect to the home page
    return redirect(url_for('home'))


@app.route('/plant/edit/<int:plant_id>', methods=['GET', 'POST'])
def edit_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    if request.method == 'POST':
        plant.common_name = request.form['common_name']
        plant.scientific_name = request.form['scientific_name']
        plant.sunlight_care = request.form['sunlight_care']
        plant.water_care = request.form['water_care']
        plant.temperature_care = request.form['temperature_care']
        plant.humidity_care = request.form['humidity_care']
        plant.growing_tips = request.form['growing_tips']
        plant.propagation_tips = request.form['propagation_tips']
        plant.common_pests = request.form['common_pests']
        plant.image_url = request.form['image_url']
        plant.family = request.form['family']
        plant.genus = request.form['genus']
        plant.year = request.form['year']
        plant.edible = request.form['edible']
        plant.edible_part = request.form['edible_part']
        plant.edible_notes = request.form['edible_notes']
        plant.medicinal = request.form['medicinal']
        plant.medicinal_notes = request.form['medicinal_notes']
        plant.toxicity = request.form['toxicity']
        plant.synonyms = request.form['synonyms']
        plant.native_status = request.form['native_status']
        plant.conservation_status = request.form['conservation_status']

        db.session.commit()
        flash('Plant details have been updated!', 'success')
        return redirect(url_for('plants'))

    return render_template('edit_plant.html', plant=plant)


@app.route('/plant/delete/<int:plant_id>', methods=['POST'])
def delete_plant(plant_id):
    plant_to_delete = Plant.query.get_or_404(plant_id)
    db.session.delete(plant_to_delete)
    db.session.commit()
    flash(f'Successfully deleted plant with ID {plant_id}', 'success')
    return redirect(url_for('list_plants'))
