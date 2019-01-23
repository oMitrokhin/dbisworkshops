from flask_wtf import FlaskForm
from wtforms import StringField,   SubmitField,  PasswordField, DateField
from flask import Flask, render_template, request, flash
from wtforms import validators, ValidationError


class RegForm(FlaskForm):

    user_email = StringField("Email: ", [
        validators.DataRequired("Please enter your email."),
        validators.Email("Wrong email format")
    ])

    password = PasswordField("Password:", [
                                             validators.DataRequired("Please enter your password."),
                                             validators.Length(3, 20, "Password should be from 3 to 20 symbols and start with capital letter")
                                          ])


    user_information = StringField("User information: ",''' [
                                                            validators.Length(0, 200, "Please enter less iformation.(max 200 symbols")
                                                        ]''')


    submit = SubmitField("Register")