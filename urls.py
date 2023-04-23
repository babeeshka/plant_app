from flask import Flask
from app import index, list_plants, search, add_plant, edit, delete

app = Flask(__name__)

app.add_url_rule('/', view_func=index)
app.add_url_rule('/plants', view_func=list_plants)
app.add_url_rule('/search', view_func=search)
app.add_url_rule('/add_plant', view_func=add_plant, methods=['GET', 'POST'])
app.add_url_rule('/edit/<int:id>', view_func=edit, methods=['GET', 'POST'])
app.add_url_rule('/delete/<int:id>', view_func=delete, methods=['POST'])