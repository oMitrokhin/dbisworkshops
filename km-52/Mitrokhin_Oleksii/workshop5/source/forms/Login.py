from flask_wtf import FlaskForm
from wtforms import StringField,   SubmitField,  PasswordField, DateField
from flask import Flask, render_template, request, flash
from wtforms import validators, ValidationError


class LoginForm(FlaskForm):

    user_email = StringField("Email: ", [
        validators.DataRequired("Please enter your email."),
        validators.Email("Wrong email format")
    ])

    password = PasswordField("Password:", [
                                             validators.DataRequired("Please enter your password."),
                                             validators.Length(3, 20, "Password should be from 3 to 20 symbols")
                                          ])

    submit = SubmitField("Log in")