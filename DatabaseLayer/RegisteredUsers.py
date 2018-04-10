from DatabaseLayer.getConn import getConn
from sqlite3 import Error
from SharedClasses.RegisteredUser import RegisteredUser

def addUser(user):
    conn = getConn()
    sql = """
            INSERT INTO RegisteredUsers(username,password)
            VALUES ('{}','{}')
            """.format(user.username, user.password)
    try:
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        conn.close()
    except Error as e:
        return False
    return True


def editUserPassword(user):
    conn = getConn()
    sql = """
            UPDATE RegisteredUsers
            SET password = '{}'
            WHERE username = '{}'
            """.format(user.password, user.username)
    try:
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        conn.close()
    except Error as e:
        return False
    return True


def getUser(username):
    conn = getConn()
    sql = """
            SELECT *
            FROM RegisteredUsers
            WHERE username = '{}'
            """.format(username)
    try:
        c = conn.cursor()
        c.execute(sql)
        user = c.fetchone()
        user = RegisteredUser(user[0], user[1],user[2])
        conn.close()
        return user
    except Error as e:
        return False

def login(user):
    conn = getConn()
    sql = """
            SELECT *
            FROM RegisteredUsers
            WHERE username = '{}' AND password = '{}'
            """.format(user.username,user.password)
    try:
        c = conn.cursor()
        c.execute(sql)
        user = c.fetchOne()
        conn.close()
        return True
    except Error as e:
        return False