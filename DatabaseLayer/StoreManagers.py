from DatabaseLayer.getConn import get_conn,commit_command
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


def add_manager(shop_id, target_user_id, permissions):
    sql = """
            INSERT INTO StoreManagers (username, shopId, 
                                        addItemPermission,
                                        editItemPermission,
                                        replyMessagePermission, 
                                        getAllMessagePermission,
                                        getPurchaseHistoryPermission)
            VALUES ('{}','{}','{}','{}','{}','{}','{}')
            """.format(target_user_id, shop_id,
                       permissions.addItemPermission,
                       permissions.editItemPermission,
                       permissions.replyMessagePermission,
                       permissions.getAllMessagePermission,
                       permissions.getPurchaseHistoryPermission)
    return commit_command(sql)
