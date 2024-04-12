from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class Conductor:
    def __init__(self, name, ganancia) -> None:
        self.name = name
        self.ganancia = ganancia
    
    def calcular_precio(self, km):
        if km > 5:
            precio_standar_km = 1200
            precio_total = round(self.ganancia * km * precio_standar_km)
            precio_total = f'$ {int(precio_total)}'
            return precio_total
        else:
            precio = '$ 7000'
            return precio


class RegisterForm(FlaskForm):
    origen = StringField(label='Origen:', validators=[DataRequired()])
    destino = StringField(label='Destino:', validators=[DataRequired()])
    submit = SubmitField(label='Buscar conductor')