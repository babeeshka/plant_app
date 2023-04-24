from flask import Flask
from app import home, list_plants, search, add_plant, edit, delete, modify

app = Flask(__name__)

app.add_url_rule('/', view_func=home)
app.add_url_rule('/plants', view_func=list_plants)
app.add_url_rule('/search', view_func=search)
app.add_url_rule('/add_plant', view_func=add_plant, methods=['GET', 'POST'])
app.add_url_rule('/edit/<int:id>', view_func=edit, methods=['GET', 'POST'])
app.add_url_rule('/delete/<int:id>', view_func=delete, methods=['POST'])
app.add_url_rule('/modify_plant/<int:id>', view_func=modify, methods=['GET', 'POST'])