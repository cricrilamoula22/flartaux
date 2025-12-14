from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
"""
class ItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Submit')
"""
from wtforms import SelectField
class Form(FlaskForm):

    commune = SelectField('commune', choices=[])
    section = SelectField('section', choices=[])
    parcelle = SelectField('parcelle', choices=[])  