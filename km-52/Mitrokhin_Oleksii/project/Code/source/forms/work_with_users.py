from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField


class UpdateUserForm(FlaskForm):
    user_list = RadioField("List of Users", coerce=int)

    change_role = SubmitField("Block/UnBlcok")

