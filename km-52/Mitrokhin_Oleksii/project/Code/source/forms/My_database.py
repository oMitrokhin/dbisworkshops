from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, StringField, SelectField, FloatField,IntegerField, validators

class UserProductForm(FlaskForm):
    product_list = RadioField('', coerce=int)
    edit_product = SubmitField('Edit')
    delete_product = SubmitField('Delete')

class UserProductEditForm(FlaskForm):
    product_price = FloatField("  Price: ", [validators.regexp('\d{1,10}', message="Price must be real number not exceeding 10 characters")])
    product_count = IntegerField("  Count: ",)
    product_priority = SelectField("  Priority: ", choices=[('Low','Low'), ('Medium','Medium'), ('High','High')])
    edit = SubmitField('Edit')
