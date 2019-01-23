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
from source.forms.Search_product import AllProductsForm,UserProductAddForm
from source.forms.Create_recomendation import RecomendationForm
from source.forms.Add_new_product import ProductAddForm

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
        role = session['role']
        return render_template('index.html', user_email=user_email, role=role)
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
        i=0
        index_list = []
        while i<len(product_list):
            index_list.append(i+1)
            i=i+1
        i=0
        product_name=[row[0] for row in product_list]
        product_price = [row[1] for row in product_list]
        product_count = [row[4] for row in product_list]
        product_priority = [row[3] for row in product_list]
        product_purchase_date=[]
        while i<len(product_list):
            product_purchase_date.append(datetime.strftime(product_list[i][2],'%Y.%m.%d'))
            i=i+1

        form.product_list.choices = [([int(index_list.index(current)), current]) for current in index_list]
        if request.method == 'POST':
            if form.validate_on_submit():
                if form.delete_product.data:
                    deleteUserProduct(session['user_email'],product_list[int(request.form['product_list'])][0],product_list[int(request.form['product_list'])][2])
                    product_list = getUserProduct(session['user_email'])
                    i=0
                    index_list = []
                    while i<len(product_list):
                        index_list.append(i+1)
                        i=i+1
                    i=0
                    product_name=[row[0] for row in product_list]
                    product_price = [row[1] for row in product_list]
                    product_count = [row[4] for row in product_list]
                    product_priority = [row[3] for row in product_list]
                    product_purchase_date=[]
                    while i<len(product_list):
                        product_purchase_date.append(datetime.strftime(product_list[i][2],'%Y.%m.%d'))
                        i=i+1
                    form.product_list.choices = [([int(index_list.index(current)), current]) for current in index_list]
                    return render_template('My_database.html', form=form,product_name=product_name,product_purchase_date=product_purchase_date, product_price=product_price, product_count=product_count, product_priority=product_priority)
                elif form.edit_product.data:
                    product_name=product_list[int(request.form['product_list'])][0]
                    product_price=product_list[int(request.form['product_list'])][1]
                    product_purchase_date = datetime.strftime(product_list[int(request.form['product_list'])][2],'%Y.%m.%d')
                    product_priority=product_list[int(request.form['product_list'])][3]
                    product_count=product_list[int(request.form['product_list'])][4]
                    session['product_name'] = product_name
                    session['product_price'] = product_price
                    session['product_purchase_date'] = product_purchase_date
                    session['product_priority'] = product_priority
                    session['product_count'] = product_count
                    return render_template('Edit_my_database.html', edit_form=edit_form, product_name=product_name,product_purchase_date=product_purchase_date, product_price=product_price, product_count=product_count, product_priority=product_priority)
                else:
                    product_list = getUserProduct(session['user_email'])
                    i=0
                    index_list = []
                    while i<len(product_list):
                        index_list.append(i+1)
                        i=i+1
                    i=0
                    product_name=[row[0] for row in product_list]
                    product_price = [row[1] for row in product_list]
                    product_count = [row[4] for row in product_list]
                    product_priority = [row[3] for row in product_list]
                    product_purchase_date=[]
                    while i<len(product_list):
                        product_purchase_date.append(datetime.strftime(product_list[i][2],'%Y.%m.%d'))
                        i=i+1
                    form.product_list.choices = [([int(index_list.index(current)), current]) for current in index_list]
                    return render_template('My_database.html', form=form,product_name=product_name,product_purchase_date=product_purchase_date, product_price=product_price, product_count=product_count, product_priority=product_priority)

        return render_template('My_database.html', form=form,product_name=product_name,product_purchase_date=product_purchase_date, product_price=product_price, product_count=product_count, product_priority=product_priority)
    else:
        return redirect(url_for('index'))

@app.route('/Edit_my_database', methods=['POST','GET'])
def Edit_my_database():

    if ((('user_email' in session) or (request.cookies.get('user_email')!= None)) and 'product_name' in session):
        if 'user_email' in session:
            user_email = session['user_email']
        else:
            user_email = request.cookies.get('user_email')
        edit_form=UserProductEditForm()
        if request.method == 'POST':
            if request.form['product_price']!='':
                product_price=float(request.form['product_price'])
            else:
                product_price=session['product_price']
            if request.form['product_count']!='':
                product_count=int(request.form['product_count'])
            else:
                product_count=session['product_count']
            product_priority=request.form['product_priority']
            product_name=session['product_name']
            product_purchase_date = session['product_purchase_date']
            editUserProduct(user_email, product_name,datetime.strptime(product_purchase_date, '%Y.%m.%d'), product_price,product_count,product_priority)
            return render_template('Edit_my_database.html', edit_form=edit_form, product_name=product_name,product_purchase_date=product_purchase_date, product_price=product_price, product_count=product_count, product_priority=product_priority)
        product_name=session['product_name']
        product_price=session['product_price']
        product_purchase_date = session['product_purchase_date']
        product_priority=session['product_priority']
        product_count=session['product_count']
        return render_template('Edit_my_database.html', edit_form=edit_form, product_name=product_name,product_purchase_date=product_purchase_date, product_price=product_price, product_count=product_count, product_priority=product_priority)

    else:
        return redirect(url_for('index'))

@app.route('/Search_product', methods=['POST','GET'])
def Search_product():
    if ('user_email' in session) or (request.cookies.get('user_email')!= None):
        if 'user_email' in session:
            user_email = session['user_email']
            role = getUserRole(user_email)
        else:
            user_email = request.cookies.get('user_email')
            role = session['role']
        form = AllProductsForm()
        edit_form=UserProductAddForm()
        product_list = getProducts()
        i=0
        index_list = []
        while i<len(product_list):
            index_list.append(i+1)
            i=i+1
        product_name=[row[0] for row in product_list]
        product_price = [row[1] for row in product_list]
        form.product_list.choices = [([int(index_list.index(current)), current]) for current in index_list]
        if request.method == 'POST':
            if form.validate_on_submit():
                if form.add_new_product.data:
                    return redirect(url_for('Add_new_product'))
                elif form.delete_button.data:
                    product_name=product_list[int(request.form['product_list'])][0]
                    deleteProductFromBase(product_name)
                    product_list = getProducts()
                    i=0
                    index_list = []
                    while i<len(product_list):
                        index_list.append(i+1)
                        i=i+1
                    product_name=[row[0] for row in product_list]
                    product_price = [row[1] for row in product_list]
                    form.product_list.choices = [([int(index_list.index(current)), current]) for current in index_list]
                    return render_template('Search_product.html',role=role, form=form, product_name=product_name,product_price=product_price)
                elif form.search_button.data:
                    search = request.form['searching_field']
                    i=0; j=0; index_list = []; search_product_name=[]; search_product_price=[]; search_product_list=[]
                    while i<len(product_list):
                        if search in product_name[i]:
                            j=j+1
                            index_list.append(j)
                            search_product_name.append(product_name[i])
                            search_product_price.append(product_price[i])
                            search_product_list.append([product_name[i],product_price[i]])
                        i=i+1
                    product_name=[]; product_name=search_product_name
                    product_price=[]; product_price=search_product_price
                    session['product_list']=search_product_list
                    form.product_list.choices = [([int(index_list.index(current)), current]) for current in index_list]
                    return render_template('Search_product.html',role=role, form=form, product_name=product_name,product_price=product_price)
                elif form.add_product.data:
                    if 'product_list' in session:
                        product_list=session['product_list']
                    product_name=product_list[int(request.form['product_list'])][0]
                    product_price=product_list[int(request.form['product_list'])][1]
                    session['product_name'] = product_name
                    session['product_price'] = product_price
                    session.pop('product_list', None)
                    return render_template('Add_product.html', edit_form=edit_form,product_name=product_name,product_price=product_price)
                #return render_template('Search_product.html',role=role, form=form, product_name=product_name,product_price=product_price)
        else:
            session.pop('product_list', None)
        return render_template('Search_product.html',role=role, form=form, product_name=product_name,product_price=product_price)
    else:
        return redirect(url_for('index'))

@app.route('/Add_product', methods=['POST','GET'])
def Add_product():
    if ((('user_email' in session) or (request.cookies.get('user_email')!= None)) and 'product_name' in session):
        if 'user_email' in session:
            user_email = session['user_email']
        else:
            user_email = request.cookies.get('user_email')
        edit_form=UserProductAddForm()
        product_name=session['product_name']
        product_price=session['product_price']
        if request.method == 'POST':
            product_user_price = float(request.form['product_price'])
            product_count = int(request.form['product_count'])
            product_purchase_date = request.form['product_purchase_date']
            product_priority = request.form['product_priority']
            if addProduct(user_email,product_name,datetime.strptime(product_purchase_date, '%Y.%m.%d'),product_user_price,product_count,product_priority)==0:
                return redirect(url_for('Search_product'))
            elif addProduct(user_email,product_name,datetime.strptime(product_purchase_date, '%Y.%m.%d'),product_user_price,product_count,product_priority)==1:
                return render_template('Add_product.html', edit_form=edit_form,product_name=product_name,product_price=product_price,message="You can't add more then one product with the same name and same purchase date! Please, edit this product in your base.")
        return render_template('Add_product.html', edit_form=edit_form,product_name=product_name,product_price=product_price)
    else:
        return redirect(url_for('index'))

@app.route('/Add_new_product', methods=['POST','GET'])
def Add_new_product():
    if ((('user_email' in session) or (request.cookies.get('user_email')!= None)) and (session['role']=='Admin' or getUserRole(request.cookies.get('user_email'))=='Admin')):
        if 'user_email' in session:
            user_email = session['user_email']
        else:
            user_email = request.cookies.get('user_email')
        form=ProductAddForm()
        if request.method == 'POST':
            product_price = float(request.form['product_price'])
            product_name = request.form['product_name']
            if addNewProductToBase(product_name,product_price)==0:
                return redirect(url_for('Search_product'))
            elif addNewProductToBase(product_name,product_price)==1:
                return render_template('Add_new_product.html', form=form, message='Product with that name already exist')
        return render_template('Add_new_product.html', form=form)
    else:
        return redirect(url_for('index'))

@app.route('/Create_recomendation', methods=['POST','GET'])
def Create_recomendation():
    if ((('user_email' in session) or (request.cookies.get('user_email')!= None)) and 'product_name' in session):
        if 'user_email' in session:
            user_email = session['user_email']
        else:
            user_email = request.cookies.get('user_email')
        form=RecomendationForm()
        if request.method=='POST':
            from_date = datetime.strptime(request.form['start_date'], '%Y.%m.%d')
            to_date = datetime.strptime(request.form['end_date'], '%Y.%m.%d')
            total_count = int(request.form['total_count'])
            recomendation_list = recomendation(user_email,from_date,to_date,total_count)
            product_name = [row[0] for row in recomendation_list]
            total_price = [row[1] for row in recomendation_list]
            product_count = [row[2] for row in recomendation_list]
            product_priority = [row[3] for row in recomendation_list]
            return render_template('Create_recomendation.html', form=form, status='visible',total_count=total_count, product_name=product_name, total_price=total_price,product_count=product_count, product_priority=product_priority)
        else:
            return render_template('Create_recomendation.html', form=form, status='in',total_count=0)

    else:
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
