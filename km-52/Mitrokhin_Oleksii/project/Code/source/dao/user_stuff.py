import cx_Oracle
from source.dao.connect_info import *


def getUserEmail(user_email):
    connection = cx_Oracle.connect(username, password, databaseName)
    cursor = connection.cursor()

    user = cursor.callfunc("P_User.get_user", cx_Oracle.STRING, [user_email])

    cursor.close()
    connection.close()

    return user


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

    query = 'SELECT * FROM "User"'
    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


def block_unblock_users(user_email):
    connection = cx_Oracle.connect(username, password, databaseName)

    cursor = connection.cursor()

    cursor.callproc("P_User.block_un_user", [user_email])
    cursor.close()
    connection.close()

    return user_email


def recomendation(user_email, from_date, to_date, count):
    connection = cx_Oracle.connect(username, password, databaseName)

    cursor = connection.cursor()

    recomendation = cursor.callfunc("P_Recomendation.get_recomendation", cx_Oracle.STRING,
                                    [user_email, from_date, to_date, count])
    cursor.close()
    connection.close()

    return recomendation
