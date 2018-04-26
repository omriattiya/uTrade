from DatabaseLayer.getConn import commit_command, select_command
from SharedClasses.StoreManager import StoreManager


def parse_store_managers(store_managers):
    store_managers_list = []
    for store_manager in store_managers:
        store_managers_list.append(StoreManager(store_manager[0], store_manager[1], store_manager[2],
                                                store_manager[3], store_manager[4], store_manager[5],
                                                store_manager[6], store_manager[7], store_manager[8]))
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


def is_store_manager(username):
    sql_query = """
                SELECT *
                FROM StoreManagers
                WHERE username = '{}'
            """.format(username)
    manager = select_command(sql_query)
    manager = parse_store_managers(manager)
    if len(manager) >= 1:
        return True
    else:
        return False


def add_manager(store_manager):
    sql = """
            INSERT INTO StoreManagers (username, shop_name, 
                                        addItemPermission,
                                        removeItemPermission,
                                        editItemPermission,
                                        replyMessagePermission, 
                                        getAllMessagePermission,
                                        getPurchaseHistoryPermission,
                                        discountPermission)
            VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}')
            """.format(store_manager.username, store_manager.store_name,
                       store_manager.permission_add_item,
                       store_manager.permission_remove_item,
                       store_manager.permission_edit_item,
                       store_manager.permission_reply_messages,
                       store_manager.permission_get_all_messages,
                       store_manager.permission_get_purchased_history,
                       store_manager.discount_permission)
    return commit_command(sql)


def remove_manager(username):
    sql = """
                    DELETE FROM StoreManagers
                    WHERE username = '{}'
                  """.format(username)
    return commit_command(sql)
