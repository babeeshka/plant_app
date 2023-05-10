from flask import Flask
from app import home, list_plants, search, search_results, add_plant, manual_entry

app = Flask(__name__)

app.add_url_rule('/', view_func=home)
app.add_url_rule('/plants', view_func=list_plants)
app.add_url_rule('/plant_information/<int:plant_id>', view_func=plant_information)
app.add_url_rule('/search', view_func=search_plant, methods=['GET', 'POST'])
app.add_url_rule('/search_results', view_func=search_results, methods=['POST'])
app.add_url_rule('/add_plant', view_func=add_plant, methods=['GET', 'POST'])
app.add_url_rule('/manual_entry', view_func=manual_entry, methods=['GET', 'POST'])
app.add_url_rule('/add_to_database', view_func=add_to_database, methods=['POST'])
