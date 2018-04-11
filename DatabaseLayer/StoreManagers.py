from DatabaseLayer.getConn import get_conn,commit_command
from sqlite3 import Error


def getStoreManager(username,shop_name):
    sql = """
                SELECT *
                FROM StoreManagers
                WHERE username = '{}' AND shop_name = '{}'
            """.format(username,shop_name)
    try:
        conn = get_conn()
        c = conn.cursor()
        c.execute(sql)
        manager = c.fetchone()
        if manager is not None:
            return manager
        else:
            return False
    except Error as e:
        return False


def add_manager(shop_name, target_username, permissions):
    sql = """
            INSERT INTO StoreManagers (username, shop_name, 
                                        addItemPermission,
                                        editItemPermission,
                                        replyMessagePermission, 
                                        getAllMessagePermission,
                                        getPurchaseHistoryPermission)
            VALUES ('{}','{}','{}','{}','{}','{}','{}')
            """.format(target_username, shop_name,
                       permissions.addItemPermission,
                       permissions.editItemPermission,
                       permissions.replyMessagePermission,
                       permissions.getAllMessagePermission,
                       permissions.getPurchaseHistoryPermission)
    return commit_command(sql)
