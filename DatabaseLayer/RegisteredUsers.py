from DatabaseLayer.getConn import getConn
from sqlite3 import Error


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
        user = c.fetchOne()
        conn.close()
        return user
    except Error as e:
        return False