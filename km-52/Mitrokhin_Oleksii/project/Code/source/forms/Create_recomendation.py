from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, StringField, SelectField, FloatField,DateField,IntegerField, validators

class RecomendationForm(FlaskForm):
    start_date = DateField("From date:", [validators.DataRequired()])
    end_date = DateField("To date:", [validators.DataRequired()])
    total_count = IntegerField("Count of different products: ", [validators.DataRequired()])
    create_recomendation = SubmitField("Create recommendation")