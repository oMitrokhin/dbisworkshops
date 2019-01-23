from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, StringField, SelectField, FloatField,DateField,IntegerField, validators

class AllProductsForm(FlaskForm):
    searching_field = StringField("Search: ")
    product_list = RadioField("", coerce=int,default='0')
    search_button = SubmitField("Search")
    add_product = SubmitField("Add product")
    add_new_product = SubmitField("Add new available product")
    delete_button = SubmitField("Delete available product")
class UserProductAddForm(FlaskForm):
    product_price = FloatField("  Price: ", [validators.DataRequired(),
                                             validators.regexp('\d{1,10}', message="Price must be real number not exceeding 10 characters")])
    product_count = IntegerField("  Count: ", [validators.DataRequired()])
    product_priority = SelectField("  Priority: ", choices=[('Low','Low'), ('Medium','Medium'), ('High','High')])
    product_purchase_date = DateField(" Purchase date: ", [validators.DataRequired()])
    edit = SubmitField('Submit')
