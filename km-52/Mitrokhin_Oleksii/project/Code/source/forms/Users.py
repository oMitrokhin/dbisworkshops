from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField

class UsersForm(FlaskForm):
    user_list = RadioField("Users list", coerce=int)
    block_user = SubmitField('Block/Unblock')
    delete_user = SubmitField('Delete')
