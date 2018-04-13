class StoreManager:
    def __init__(self, username, store_name, permission_add_item, permission_remove_item, permission_edit_item,
                 permission_reply_messages, permission_get_all_messages, permission_get_purchased_history):
        self.username = username
        self.store_name = store_name
        self.permission_add_item = permission_add_item
        self.permission_remove_item = permission_remove_item
        self.permission_edit_item = permission_edit_item
        self.permission_reply_messages = permission_reply_messages
        self.permission_get_all_messages = permission_get_all_messages
        self.permission_get_purchased_history = permission_get_purchased_history

    @classmethod
    def store_manager(cls, username, store_name, permissions):
        return StoreManager(username,
                            store_name,
                            permissions.get('permission_add_item', 0),
                            permissions.get('permission_remove_item', 0),
                            permissions.get('permission_edit_item', 0),
                            permissions.get('permission_reply_messages', 0),
                            permissions.get('permission_get_all_messages', 0),
                            permissions.get('permission_get_purchased_history', 0))
