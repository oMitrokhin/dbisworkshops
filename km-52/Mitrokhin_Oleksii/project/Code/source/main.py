import cx_Oracle
from flask import Flask, make_response, render_template, session, request, redirect, url_for
from datetime import date, datetime
from source.forms.Login import LoginForm
from source.forms.registration import RegForm
from source.dao.connect_info import *
from source.dao.user_stuff import *
from datetime import datetime, timedelta
from source.forms.Users import UsersForm
from source.forms.My_database import UserProductForm,UserProductEditForm
from source.forms.Search_product import AllProductsForm

app = Flask(__name__)

app.secret_key = 'mykey'
@app.route('/')
def index():

    if 'user_email' in session:
        user_email = session['user_email']
        role = session['role']
        return render_template('index.html', user_email=user_email, role=role)
    elif request.cookies.get('user_email')!= None:
        user_email = request.cookies.get('user_email')
        session['user_email'] = user_email
        session['role'] = getUserRole(user_email)
        return render_template('index.html', user_email=user_email, role='Cookies!')
    else:
        login_form = LoginForm()
        return render_template('login.html', form=login_form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()

    if request.method == 'POST':
        connection = cx_Oracle.connect(username, password, databaseName)
        cursor = connection.cursor()
        cursor.execute('select * from "User"')
        users = cursor.fetchall()
        cursor.close()
        connection.close()
        login_user = request.form['user_email']

        if request.form['user_email'] in [row[0] for row in users]:
            if request.form['password'] == getUserPass(login_user):
                session['user_email'] = request.form['user_email']
                session['role'] = getUserRole(request.form['user_email'])
                resp = make_response(redirect(url_for('index')))
                expires = datetime.now()
                expires += timedelta(weeks=2)
                resp.set_cookie('user_email', login_user, expires=expires)
                return resp
            else:
                return render_template('login.html', form=login_form, message='You entered wrong passsword!')
        else:
            return render_template('login.html', form=login_form, message='User with current login does not exists.')

    return render_template('login.html', form=login_form)

@app.route('/registration', methods=['POST', 'GET'])
def registration():
    form = RegForm()

    if request.method == 'POST':
        connection = cx_Oracle.connect(username, password, databaseName)
        cursor = connection.cursor()
        cursor.execute('select * from "User"')
        users = cursor.fetchall()
        cursor.close()
        connection.close()

        if request.form['user_email'] in [row[0] for row in users]:
            return render_template('registration.html', form=form, message='User with current email already exists.')
        else:
            regUser(request.form['user_email'],request.form['password'],request.form['user_information'])
            session['user_email'] = request.form['user_email']
            session['role'] = getUserRole(request.form['user_email'])
            resp = make_response(redirect(url_for('index')))
            expires = datetime.now()
            expires += timedelta(weeks=2)
            resp.set_cookie('user_email', request.form['user_email'], expires=expires)
            return resp

    return render_template('registration.html', form=form)

@app.route('/logout')
def logout():
    user_email=session['user_email']
    session.pop('user_email', None)
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('user_email', user_email, expires=0)
    return resp

@app.route('/Users', methods=['POST','GET'])
def users():
    if ('user_email' in session) or (request.cookies.get('user_email')!= None):
        if 'user_email' in session:
            user_email = session['user_email']
        else:
            user_email = request.cookies.get('user_email')
        if getUserRole(user_email)=='Admin':
            form=UsersForm()
            users_list = getUsers()
            form.user_list.choices = [([int(users_list.index(current)), current]) for current in users_list]
            if request.method == 'POST':
                if form.validate_on_submit():
                    if form.block_user.data:
                        blockUser(users_list[int(request.form['user_list'])][0])
                    elif form.delete_user.data:
                        deleteUser(users_list[int(request.form['user_list'])][0])
                users_list = getUsers()
                form.user_list.choices = [([int(users_list.index(current)), current]) for current in users_list]
                return render_template('Users.html', form=form)
            return render_template('Users.html', form=form)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


@app.route('/My_database', methods=['POST','GET'])
def My_database():
    if ('user_email' in session) or (request.cookies.get('user_email')!= None):
        if 'user_email' in session:
            user_email = session['user_email']
        else:
            user_email = request.cookies.get('user_email')
        form=UserProductForm()
        edit_form=UserProductEditForm()
        product_list = getUserProduct(session['user_email'])
        product_date = [row[2] for row in product_list]
        i=0
        """
        while i<len(product_list):
            product_purchase_date = datetime.strftime(product_date[i],'%Y.%m.%d')
            print(product_purchase_date)
            i=i+1
        """
        form.product_list.choices = [([int(product_list.index(current)), current]) for current in product_list]
        if request.method == 'POST':
            if form.validate_on_submit():
                if form.delete_product.data:
                    deleteUserProduct(session['user_email'],product_list[int(request.form['product_list'])][0],product_list[int(request.form['product_list'])][2])
                    product_list = getUserProduct(session['user_email'])
                    form.product_list.choices = [([int(product_list.index(current)), current]) for current in product_list]
                    return render_template('My_database.html', form=form)
                elif form.edit_product.data:
                    product_name=product_list[int(request.form['product_list'])][0]
                    product_price=product_list[int(request.form['product_list'])][1]
                    product_purchase_date = product_list[int(request.form['product_list'])][2]
                    product_priority=product_list[int(request.form['product_list'])][3]
                    product_count=product_list[int(request.form['product_list'])][4]
                    print(datetime.date(product_purchase_date))
                    print(product_purchase_date)
                    return render_template('Edit_my_database.html', edit_form=edit_form)
                else:
                    product_list = getUserProduct(session['user_email'])
                    form.product_list.choices = [([int(product_list.index(current)), current]) for current in product_list]
                    return render_template('My_database.html', form=form)

        return render_template('My_database.html', form=form)
    else:
        return redirect(url_for('index'))

@app.route('/Edit_my_database', methods=['POST','GET'])
def Edit_my_database():
    edit_form=UserProductEditForm()
    return render_template('Edit_my_database.html', edit_form=edit_form)

@app.route('/Search_product', methods=['POST','GET'])
def Search_product():
    form = AllProductsForm()


    return render_template('Search_product.html', form=form)



if __name__ == "__main__":
    app.run(debug=True)
