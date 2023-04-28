from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class AddPlantForm(FlaskForm):
    common_name = StringField('Plant Name')
    submit = SubmitField('Search')
