import os
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_wtf.csrf import CSRFProtect
from random import randint, randrange
import secrets
import json

from database import db
from models import Plant
from plant_info import get_plant_info
from dotenv import load_dotenv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# generate a random 16-byte string and use it as the secret key
app.config['SECRET_KEY'] = secrets.token_hex(16)
csrf = CSRFProtect(app)

load_dotenv()

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


# app.py
@app.route('/')
def home():
    plants = Plant.query.all()
    if plants:
        random_index = randrange(len(plants))
        random_plant = plants[random_index]
    else:
        random_plant = None
    return render_template('home.html', plants=plants, random_plant=random_plant)


@app.route('/plants')
def list_plants():
    plants = Plant.query.all()
    return render_template('list_plants.html', plants=plants)


@app.route('/search_plant', methods=['GET', 'POST'])
def search_plant():
    if request.method == 'POST':
        query = request.form['query']
        plant = Plant.query.filter_by(common_name=query).first()
        if plant:
            return render_template('search_results.html', plant=plant)
        else:
            data = get_plant_info(query)
            return render_template('search_results.html', data=data, query=query)
    return render_template('search_plant.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    plant = Plant.query.get_or_404(id)

    if request.method == 'POST':
        plant.name = request.form['name']
        plant.sunlight = request.form['sunlight']
        plant.water = request.form['water']
        plant.temperature = request.form['temperature']
        db.session.commit()

        flash(f"{plant.name} has been updated", "success")
        return redirect(url_for("index"))

    return render_template("edit_plant.html", plant=plant)


@app.route('/modify_plant/<int:id>', methods=['GET', 'POST'])
def modify_plant(id):
    plant = Plant.query.get_or_404(id)
    if request.method == 'POST':
        try:
            plant_name = request.form['name']
            plant_info = get_plant_info(plant_name)
            if plant_info:
                plant.common_name = plant_info.get(
                    'common_name', plant_info['scientific_name'])
                plant.scientific_name = plant_info['scientific_name']
                plant.sunlight_care = request.form.get('sunlight')
                plant.water_care = request.form.get('water')
                plant.temperature_care = request.form.get('temperature')
                plant.image_url = plant_info.get('image_url')
                plant.family = plant_info.get('family')
                plant.genus = plant_info.get('genus')
                plant.year = plant_info.get('year')
                plant.edible = plant_info.get('edible')
                plant.edible_part = plant_info.get('edible_part')
                plant.edible_notes = plant_info.get('edible_notes')
                plant.medicinal = plant_info.get('medicinal')
                plant.medicinal_notes = plant_info.get('medicinal_notes')
                plant.toxicity = plant_info.get('toxicity')
                plant.synonyms = plant_info.get('synonyms')
                plant.native_status = plant_info.get('native_status')
                plant.conservation_status = plant_info.get(
                    'conservation_status')

                db.session.commit()
                flash(f"{plant.common_name} has been modified", "success")
                return redirect(url_for('home'))
            else:
                flash(
                    f"Could not find any information for plant {plant_name}.")
        except Exception as e:
            db.session.rollback()
            print(str(e))
            flash(f"Error modifying plant {plant_name}: {str(e)}", "danger")

    return render_template('modify_plant.html', plant=plant)


@app.route('/add_to_database', methods=['POST'])
def add_to_database():
    form_data = request.form
    plant_name = form_data['plant_name']

    # Get plant information
    plant_info = get_plant_info(plant_name)
    if not plant_info:
        return 'Could not find plant information'

    # Create new plant instance
    plant = Plant(
        name=plant_name,
        common_name=plant_info['common_name'],
        scientific_name=plant_info['scientific_name'],
        image_url=plant_info['image_url'],
        family=plant_info['family'],
        genus=plant_info['genus'],
        year=plant_info['year'],
        edible=plant_info['edible'],
        edible_part=plant_info['edible_part'],
        edible_notes=plant_info['edible_notes'],
        medicinal=plant_info['medicinal'],
        medicinal_notes=plant_info['medicinal_notes'],
        toxicity=plant_info['toxicity'],
        synonyms=plant_info['synonyms'],
        native_status=plant_info['native_status'],
        conservation_status=plant_info['conservation_status']
    )

    # Add plant instance to the database
    db.session.add(plant)
    db.session.commit()

    return f'Successfully added {plant_name} to the database!'


@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    plant = Plant.query.get_or_404(id)
    db.session.delete(plant)
    db.session.commit()

    flash(f"{plant.name} has been deleted", "success")
    return redirect(url_for("index"))
