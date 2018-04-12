from DatabaseLayer.getConn import commit_command, select_command
from SharedClasses.StoreManager import StoreManager


def parse_store_managers(store_managers):
    store_managers_list = []
    for store_manager in store_managers:
        store_managers_list.append(StoreManager(store_manager[0], store_manager[1], store_manager[2],
                                                store_manager[3], store_manager[4], store_manager[5],
                                                store_manager[6], store_manager[7]))
    return store_managers_list


def get_store_manager(username, shop_name):
    sql_query = """
                SELECT *
                FROM StoreManagers
                WHERE username = '{}' AND shop_name = '{}'
            """.format(username, shop_name)
    manager = select_command(sql_query)
    manager = parse_store_managers(manager)
    if len(manager) == 1:
        return manager[0]
    else:
        return False


def add_manager(shop_name, target_username, permissions):
    sql = """
            INSERT INTO StoreManagers (username, shop_name, 
                                        addItemPermission,
                                        removeItemPermission,
                                        editItemPermission,
                                        replyMessagePermission, 
                                        getAllMessagePermission,
                                        getPurchaseHistoryPermission)
            VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')
            """.format(target_username, shop_name,
                       permissions.get('addItemPermission'),
                       permissions.get('removeItemPermission'),
                       permissions.get('editItemPermission'),
                       permissions.get('replyMessagePermission'),
                       permissions.get('getAllMessagePermission'),
                       permissions.get('getPurchaseHistoryPermission'))
    return commit_command(sql)
