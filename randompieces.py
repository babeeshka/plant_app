""" @app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Process form data and save to database
        pass
    else:
        # Get columns from the database table
        cursor = db.session.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'plants'"))
        columns = [row[0] for row in cursor.fetchall()]
        return render_template('add_plant.html', columns=columns)
     """

"""@app.route('/add_plant', methods=['GET', 'POST'])
def add_plant():
    if request.method == 'POST':
        common_name = request.form.get('common_name')
        scientific_name = request.form.get('scientific_name')
        sunlight_care = request.form.get('sunlight_care')
        water_care = request.form.get('water_care')
        temperature_care = request.form.get('temperature_care')
        humidity_care = request.form.get('humidity_care')
        growing_tips = request.form.get('growing_tips')
        propagation_tips = request.form.get('propagation_tips')
        common_pests = request.form.get('common_pests')
        family = request.form.get('family')
        genus = request.form.get('genus')
        year = request.form.get('year')
        edible = request.form.get('edible')
        edible_part = request.form.get('edible_part')
        edible_notes = request.form.get('edible_notes')
        medicinal = request.form.get('medicinal')
        medicinal_notes = request.form.get('medicinal_notes')
        toxicity = request.form.get('toxicity')
        synonyms = request.form.get('synonyms')
        native_status = request.form.get('native_status')
        conservation_status = request.form.get('conservation_status')
        
        if common_name and scientific_name:
            plant = Plant(
                common_name=common_name, 
                scientific_name=scientific_name, 
                sunlight_care=sunlight_care, 
                water_care=water_care, 
                temperature_care=temperature_care, 
                humidity_care=humidity_care, 
                growing_tips=growing_tips, 
                propagation_tips=propagation_tips, 
                common_pests=common_pests,
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
            db.session.add(plant)
            db.session.commit()
            flash(f"{common_name} has been added to your collection", "success")
            return redirect(url_for('index'))

    return render_template('add_plant.html')
"""