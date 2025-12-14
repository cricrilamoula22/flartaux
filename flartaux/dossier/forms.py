from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
"""
class ItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Submit')
"""    
 
class Form(FlaskForm):
    no_interne = StringField('no_interne')
    u_nom_raison_sociale = StringField('u_nom_raison_sociale')
    no_pacage_demandeur = StringField('no_pacage_demandeur')
