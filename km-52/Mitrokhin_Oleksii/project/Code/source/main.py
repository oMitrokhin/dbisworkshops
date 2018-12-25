from flask import Flask, render_template, request, flash, session, url_for, redirect, make_response
from source.forms.Login import LoginForm
from source.forms.registration import RegForm
from source.dao.user_stuff import *
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'development key'

@app.route('/')
def index():
    if 'user_email' in session:
        user_email = session['user_email']
        session['role'] = getUserEmail(user_email)[0][1]
        role = session['role']
        if user_email is None:
            return "<div>You are not logged in <br><a href = '/login'></b>" + "Log in</b></a><br>" + \
                   "<a href='/registration'></b>Create new account</b></a></div>"
        return render_template('index.html', user_email=user_email, role=role)
    else:
        user_email = request.cookies.get('user_email')
        session['user_email'] = user_email
        session['role'] = getUserEmail(user_email)[0][1]
        role = session['role']
        if user_email is None:
            return "<div>You are not logged in <br><a href = '/login'></b>" + "Click here to log in</b></a><br>" + \
                   "<a href='/registration'></b>Or here to create an account</b></a></div>"
        else:
            return render_template('index.html', user_email=user_email, role=role)

@app.route('/login',methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if request.method == 'POST':
        if getUserEmail(request.form['user_email']) is None:
            return render_template('login.html', form=login_form, message='User with current login does not exists.')
        else:
            user = getUserEmail(request.form['user_email'])
            if user[1] != request.form['password']:
                return render_template('login.html', form=login_form, message='You entered wrong passsword!')
            else:
                if login_form.validate():
                    session['user_email'] = request.form['user_email']
                    response = make_response(redirect(url_for('index')))
                    expires = datetime.now()
                    expires += timedelta(weeks=10)
                    response.set_cookie('user_email', request.form['user_email'], expires=expires)
                    return response
                else:
                    return render_template('login.html', form=login_form)
    else:
        if 'user_email' in session:
            return render_template('login.html', form=login_form)
        else:
            user_email = request.cookies.get('user_email')
            session['user_email'] = user_email
            if user_email is None:
                return render_template('login.html', form=login_form)
            else:
                return redirect(url_for('index'))

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    reg_form = RegForm()

    if request.method == 'POST':
        if not reg_form.validate():
            return render_template('registration.html', form=reg_form)
        else:
            if getUserEmail(request.form['user_email']) is None:
                return render_template('registration.html', form=reg_form, is_unique='User with current login already exists.')
            else:
                message = regUser(
                    request.form['user_email'],
                    request.form['password'],
                    request.form['user_information']
                )

                if message != 'Operation successful':
                    return render_template('registration.html', form=reg_form, message=message)

                session['user_email'] = request.form['user_email']
                response = make_response(redirect(url_for('index')))
                expires = datetime.now()
                expires += timedelta(weeks=2)
                response.set_cookie('user_email', request.form['user_email'], expires=expires)
                return response

    return render_template('registration.html', form=reg_form)

@app.route('/logout')
def logout():
    session.pop('user_email', None)
    response = make_response(redirect(url_for('index')))
    response.set_cookie('user_email', '', expires=0)
    return response

if __name__ == '__main__':
    app.run(debug=True)