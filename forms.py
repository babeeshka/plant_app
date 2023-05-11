from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired()])
    common_name = StringField('Common Name', validators=[DataRequired()])
    submit = SubmitField('Search')
