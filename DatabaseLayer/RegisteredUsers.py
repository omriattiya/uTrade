from DatabaseLayer.getConn import get_conn
from sqlite3 import Error
from SharedClasses.RegisteredUser import RegisteredUser


def addUser(user):
    conn = get_conn()
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
    conn = get_conn()
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


def get_user(username):
    conn = get_conn()
    sql = """
            SELECT *
            FROM RegisteredUsers
            WHERE username = '{}'
            """.format(username)
    try:
        c = conn.cursor()
        c.execute(sql)
        user = c.fetchone()
        user = RegisteredUser(user[0], user[1])
        conn.close()
        return user
    except Error as e:
        return False


def login(user):
    conn = get_conn()
    sql = """
            SELECT *
            FROM RegisteredUsers
            WHERE username = '{}' AND password = '{}'
            """.format(user.username, user.password)
    try:
        c = conn.cursor()
        c.execute(sql)
        user = c.fetchOne()
        conn.close()
        return True
    except Error as e:
        return False


def remove_user(registered_user):
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
                DELETE FROM RegisteredUsers
                WHERE username = {}
              """.format(registered_user))
    return c.fetchall()  # TODO: yoni that is not what you should return here. (True or False is)
