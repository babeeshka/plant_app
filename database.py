from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def configure_database(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:WbMa01523@localhost/plant_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
