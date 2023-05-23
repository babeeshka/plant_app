from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


def configure_database(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)


# Define db_session after configure_database
db_session = db.session
