import cx_Oracle
from source.dao.connect_info import *
from datetime import date, datetime

def getUserIndex(user_email):
    connection = cx_Oracle.connect(username, password, databaseName)
    cursor = connection.cursor()
    cursor.execute('select * from "User"')
    result = cursor.fetchall()
    index_m = [row[0] for row in result].index(user_email)
    cursor.close()
    return index_m


def getUserPass(user_email):
    connection = cx_Oracle.connect(username, password, databaseName)
    cursor = connection.cursor()
    cursor.execute('select * from "User"')
    result = cursor.fetchall()
    user_pass = result[getUserIndex(user_email)][2]
    return user_pass


def getUserRole(user_email):
    connection = cx_Oracle.connect(username, password, databaseName)
    cursor = connection.cursor()
    cursor.execute('select * from "User"')
    result = cursor.fetchall()
    user_role = result[getUserIndex(user_email)][1]
    return user_role


def regUser(user_email, user_password, user_information):
    connection = cx_Oracle.connect(username, password, databaseName)
    cursor = connection.cursor()

    cursor.callproc("User_auth.registration", [user_email, user_password, user_information])
    cursor.close()
    connection.close()

    return user_email


def getUsers():
    connection = cx_Oracle.connect(username, password, databaseName)

    cursor = connection.cursor()

    query = 'SELECT * FROM table(P_User.get_users_list)'
    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


def blockUser(user_email):
    connection = cx_Oracle.connect(username, password, databaseName)
    cursor = connection.cursor()

    cursor.callproc("P_User.block_un_user", [user_email])

    cursor.close()
    connection.close()
    return user_email

def deleteUser(user_email):
    connection = cx_Oracle.connect(username, password, databaseName)
    cursor = connection.cursor()

    cursor.callproc("P_User.delete_user", [user_email])

    cursor.close()
    connection.close()
    return user_email

def getUserProduct(user_email):
    connection = cx_Oracle.connect(username, password, databaseName)

    cursor = connection.cursor()

    query = 'SELECT * FROM table(P_user_product.get_user_product(:user_email))'
    cursor.execute(query, user_email=user_email)
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result

def deleteUserProduct(user_email, product_name, purchase_date):
    connection = cx_Oracle.connect(username, password, databaseName)
    cursor = connection.cursor()

    cursor.callproc("P_user_product.delete_user_product", [user_email, product_name, purchase_date])

    cursor.close()
    connection.close()
    return product_name

def editUserProduct(user_email, product_name, purchase_date, product_price, product_count, product_priority):
    connection = cx_Oracle.connect(username,password,databaseName)
    cursor = connection.cursor()

    cursor.callproc("P_user_product.edit_product_in_userbase", [user_email, product_name, purchase_date, product_price, product_count, product_priority])

    cursor.close()
    connection.close()
    return product_name

def getProducts():
    connection = cx_Oracle.connect(username, password, databaseName)

    cursor = connection.cursor()

    query = 'SELECT * FROM table(P_Av_PR.get_available_product())'
    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result

def addProduct(user_email, product_name, purchase_date, user_product_price, product_count, product_priority):
    connection = cx_Oracle.connect(username, password, databaseName)
    product_list = getUserProduct(user_email)
    prod_name = [row[0] for row in product_list]
    product_purchase_date=[]; i=0; pr_list=[]
    while i<len(product_list):
        product_purchase_date.append(datetime.strftime(product_list[i][2],'%Y-%m-%d'))
        pr_list.append([prod_name[i],product_purchase_date[i]])
        i=i+1
    if [product_name,datetime.strftime(purchase_date,'%Y-%m-%d')] in pr_list:
        connection.close()
        return 1
    else:
        cursor = connection.cursor()
        cursor.callproc("P_user_product.add_product_to_userbase", [user_email, product_name, purchase_date, user_product_price, product_count, product_priority])
        cursor.close()
        connection.close()
        return 0

def deleteProductFromBase(product_name):
    connection = cx_Oracle.connect(username, password, databaseName)
    cursor = connection.cursor()

    cursor.callproc("P_Av_PR.delete_product_from_base", [product_name])

    cursor.close()
    connection.close()
    return product_name

def addNewProductToBase(product_name,product_price):
    connection = cx_Oracle.connect(username, password, databaseName)
    product_list = getProducts()
    if product_name in ([row[0] for row in product_list]):
        connection.close()
        return 1
    else:
        cursor = connection.cursor()
        cursor.callproc("P_Av_PR.add_product_to_base", [product_name, product_price])
        cursor.close()
        connection.close()
        return 0

def recomendation(user_email, from_date, to_date, count):
    connection = cx_Oracle.connect(username, password, databaseName)

    cursor = connection.cursor()

    query = 'SELECT * FROM TABLE (P_Recomendation.get_recomendation(:check_email, :start_date, :end_date, :total_count))'
    cursor.execute(query,check_email = user_email, start_date = from_date, end_date = to_date, total_count = count)
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result
