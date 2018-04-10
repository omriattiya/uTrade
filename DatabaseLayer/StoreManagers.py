from DatabaseLayer.getConn import commit_command


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
