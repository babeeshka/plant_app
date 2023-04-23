
from random import randint
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
import secrets
from database import db
from models import Plant
import datetime
from random import randrange
from plant_info import get_plant_info
import logging
from logging.handlers import RotatingFileHandler
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.config['SECRET_KEY'] = secrets.token_hex(16)  # generate a random 16-byte string and use it as the secret key
csrf = CSRFProtect(app)

# Set the logging level to "DEBUG"
app.logger.setLevel(logging.DEBUG)

# Add a rotating file handler that writes messages to a log file
log_file = 'app.log'
file_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=5)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)

# app.py
@app.route('/')
def index():
    plants = Plant.query.all()
    random_plant = plants[randint(0, len(plants)-1)] if plants else None
    return render_template('home.html', plants=plants, random_plant=random_plant, random=randint)

@app.route('/home')
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

@app.route('/plant/search', methods=['GET'])
def plant_search():
    query = request.args.get('query')
    plants = Plant.plant_search(query)
    if plants:
        return render_template('search_results.html', plants=plants, query=query)
    else:
        flash(f'Could not find any plants with name {query}.')
        return redirect(url_for('list_plants'))

@app.route('/add_plant', methods=['GET', 'POST'])
def add_plant():
    if request.method == 'POST':
        try:
            plant_name = request.form['name']
            plant_info = get_plant_info(plant_name)

            if plant_info:
                new_plant = Plant(
                    common_name=plant_info['common_name'] or plant_info['scientific_name'],
                    scientific_name=plant_info['scientific_name'],
                    sunlight_care=request.form['sunlight'],
                    water_care=request.form['water'],
                    temperature_care=request.form['temperature'],
                    image_url=plant_info['image_url']
                )

                db.session.add(new_plant)
                db.session.commit()

                flash(f"{new_plant.common_name} has been added", "success")
                return redirect(url_for('index'))
            else:
                flash(f"Could not find any information for plant {plant_name}.")
        except Exception as e:
            db.session.rollback()
            print(str(e))
            flash(f"Error adding plant {plant_name}: {str(e)}", "danger")

    return render_template('add_plant.html')

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

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    plant = Plant.query.get_or_404(id)
    db.session.delete(plant)
    db.session.commit()

    flash(f"{plant.name} has been deleted", "success")
    return redirect(url_for("index"))
