from sqlalchemy import or_, any_, text, func
import os
import logging
from logging.handlers import RotatingFileHandler
from random import randrange
import secrets

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from database import configure_database, db
from models import Plant
from plant_info import get_plant_info
from dotenv import load_dotenv
from forms import SearchForm

PERENUAL_API_KEY = os.getenv('PERENUAL_API_KEY')

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
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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
        plants = db.session.query(Plant).filter(or_(
            Plant.common_name.ilike(f'%{query}%'),
            func.array_to_string(Plant.scientific_name, ' ').ilike(f'%{query}%')
        )).all()
        if plants:
            print("Plants found in the database:", plants)  # Debugging print statement
            # If the plant is found in the database, show the plant info
            return render_template('plant_info.html', plants=plants, query=query)
        else:
            print("No plants found in the database, fetching data from the Perenual API")  # Debugging print statement
            # If the plant is not found in the database, fetch the data from the Perenual API
            fetched_plant_info = get_plant_info(query.strip(), get_detailed_info)
            if fetched_plant_info:
                # Process the fetched plant info and display the search results
                # Instead of rendering the search_results.html template, redirect to the get_detailed_info route
                return redirect(url_for('get_detailed_info', plant_id=fetched_plant_info['id']))
            else:
                print("No plant data found in the Perenual API")  # Debugging print statement
                # If the plant data is not found in the Perenual API, show a message to the user
                flash(f'No plant named "{query}" found.')
                return redirect(url_for('home'))
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


@app.route('/get_detailed_info', methods=['POST'])
def get_detailed_info():
    plant_id = request.form['plant_id']
    detail_url = f'https://perenual.com/api/species/details/{plant_id}/?key={PERENUAL_API_KEY}'
    response = request.get(detail_url)

    if response.status_code == 200:
        plant_details = response.json()
        return render_template('detailed_search_results.html', plant_details=plant_details)
    else:
        # Handle error case
        return f"Failed to retrieve plant details for plant ID: {plant_id}"



@app.route('/plant_information/<int:plant_id>')
def plant_information(plant_id):
    # Get the plant information from the database
    plant = db_session.query(Plant).filter(Plant.id == plant_id).first()
    return render_template('plant_info.html', plant=plant)


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

    # app.logger.debug('Request headers: %s', request.headers)
    # app.logger.debug('Request body: %s', request.get_data())
    print(request.form)

    # TODO: update the request params to match Plant class in models.py
    # Retrieve the data for the new plant from the form
    common_name = request.form.get('common_name') or None
    scientific_name = request.form.get('scientific_name') or None
    other_name = request.form.get('other_name') or None
    family = request.form.get('family') or None
    type = request.form.get('type') or None
    sunlight = request.form.get('sunlight') or None
    watering = request.form.get('watering') or None
    drought_tolerant = request.form.get('drought_tolerant') or None
    origin = request.form.get('origin') or None
    soil = request.form.get('soil') or None
    growth_rate = request.form.get('growth_rate') or None
    propagation = request.form.get('propagation') or None
    pest_susceptibility = request.form.get('pest_susceptibility') or None
    description = request.form.get('description') or None
    type = request.form.get('type') or None
    cycle = request.form.get('cycle') or None
    attracts = request.form.get('attracts') or None
    invasive = request.form.get('invasive') or None
    tropical = request.form.get('tropical') or None
    edible_fruit = request.form.get('edible_fruit') or None
    edible_leaf = request.form.get('edible_leaf') or None
    medicinal = request.form.get('medicinal') or None
    harvest_season = request.form.get('harvest_season') or None
    poisonous_to_humans = request.form.get('poisonous_to_humans') or None
    poisonous_to_pets = request.form.get('poisonous_to_pets') or None
    rare = request.form.get('rare') or None

    print("Form data retrieved successfully")  # Debugging print statement

    # TODO: update the new_plant object to match the Plant class in models.py. different params now
    # Create a new Plant object with the retrieved data
    new_plant = Plant(
        common_name=common_name,
        scientific_name=scientific_name,
        other_name=other_name,
        description=description,
        sunlight=sunlight,
        watering=watering,
        origin=origin,
        type=type,
        family=family,
        soil=soil,
        drought_tolerant=drought_tolerant,
        growth_rate=growth_rate,
        propagation=propagation,
        pest_susceptibility=pest_susceptibility,
        cycle=cycle,
        attracts=attracts,
        invasive=invasive,
        tropical=tropical,
        edible_fruit=edible_fruit,
        edible_leaf=edible_leaf,
        medicinal=medicinal,
        harvest_season=harvest_season,
        poisonous_to_humans=poisonous_to_humans,
        poisonous_to_pets=poisonous_to_pets,
        rare=rare
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
        # TODO: Updatethe edit plant fields to match the incoming edit_plant.html form fields
        plant.common_name = request.form['common_name']
        plant.scientific_name = request.form['scientific_name']
        plant.other_name = request.form['other_name']
        plant.family = request.form['family']
        plant.origin = request.form['origin']
        plant.type = request.form['type']
        plant.dimension = request.form['dimension']
        plant.cycle = request.form['cycle']
        plant.attracts = request.form['attracts']
        plant.propagation = request.form['propagation']
        plant.hardiness = request.form['hardiness']
        plant.hardiness_location = request.form['hardiness_location']
        plant.watering = request.form['watering']
        plant.sunlight = request.form['sunlight']
        plant.maintenance = request.form['maintenance']
        plant.care_guides = request.form['care_guides']
        plant.soil = request.form['soil']
        plant.growth_rate = request.form['growth_rate']
        plant.drought_tolerant = request.form['drought_tolerant']
        plant.salt_tolerant = request.form['salt_tolerant']
        plant.thorny = request.form['thorny']
        plant.invasive = request.form['invasive']
        plant.tropical = request.form['tropical']
        plant.indoor = request.form['indoor']
        plant.care_level = request.form['care_level']
        plant.pest_susceptibility = request.form['pest_susceptibility']
        plant.pest_susceptibility_api = request.form['pest_susceptibility_api']
        plant.flowers = request.form['flowers']
        plant.flowering_season = request.form['flowering_season']
        plant.flower_color = request.form['flower_color']
        plant.cones = request.form['cones']
        plant.fruits = request.form['fruits']
        plant.edible_fruit = request.form['edible_fruit']
        plant.edible_fruit_taste_profile = request.form['edible_fruit_taste_profile']
        plant.fruit_nutritional_value = request.form['fruit_nutritional_value']
        plant.fruit_color = request.form['fruit_color']
        plant.harvest_season = request.form['harvest_season']
        plant.harvest_method = request.form['harvest_method']
        plant.leaf = request.form['leaf']
        plant.leaf_color = request.form['leaf_color']
        plant.edible_leaf = request.form['edible_leaf']
        plant.edible_leaf_taste_profile = request.form['edible_leaf_taste_profile']
        plant.leaf_nutritional_value = request.form['leaf_nutritional_value']
        plant.cuisine = request.form['cuisine']
        plant.cuisine_list = request.form['cuisine_list']
        plant.medicinal = request.form['medicinal']
        plant.medicinal_use = request.form['medicinal_use']
        plant.medicinal_method = request.form['medicinal_method']
        plant.poisonous_to_humans = request.form['poisonous_to_humans']
        plant.poison_effects_to_humans = request.form['poison_effects_to_humans']
        plant.poison_to_humans_cure = request.form['poison_to_humans_cure']
        plant.poisonous_to_pets = request.form['poisonous_to_pets']
        plant.rare = request.form['rare']

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
