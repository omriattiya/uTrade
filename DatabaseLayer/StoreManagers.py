from DatabaseLayer.getConn import get_conn
from sqlite3 import Error


def getStoreManager(username):
    sql = """
                SELECT *
                FROM StoreManagers
                WHERE username = '{}'
            """
    try:
        conn = get_conn()
        c = conn.cursor()
        c.execute(sql)
        manager = c.fetchone()
        return manager
    except Error as e:
        return False
