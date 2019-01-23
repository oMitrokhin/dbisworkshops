from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, StringField, SelectField, FloatField,DateField,IntegerField, validators


class ProductAddForm(FlaskForm):
    product_name = StringField("Product name: ")
    product_price = FloatField("Average price: ", [validators.DataRequired(),
                                             validators.regexp('\d{1,10}', message="Price must be real number not exceeding 10 characters")])
    add_button = SubmitField("Add")