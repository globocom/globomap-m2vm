from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired

class MetalForm (FlaskForm):
    metal_name = StringField ('Maquina fisica', validators = [DataRequired()])
    submit = SubmitField('Procurar')
