import hashlib
import re
from time import gmtime, strftime
from DatabaseLayer import RegisteredUsers, Owners, StoreManagers, Shops, SystemManagers, Discount, UserDetails,HistoryAppointings

min_password_len = 6


def register(user):
    if user.username is not None and user.password is not None and not SystemManagers.is_system_manager(user.username):
        if re.match(r'[A-Za-z0-9]{8,20}', user.username):
            if re.match(r'[A-Za-z0-9]{8,20}', user.password):
                user.password = hashlib.sha256(user.password.encode()).hexdigest()
                if Shops.search_shop(user.username) is not False:
                    return 'FAILED: Username is already taken'
                if RegisteredUsers.get_user(user.username) is not False:
                    return 'FAILED: Username is already taken'
                if RegisteredUsers.add_user(user):
                    UserDetails.insert(user.username)
                    return 'SUCCESS'
                return 'FAILED'
            else:
                return 'FAILED: Password must be 8 to 20 alphabetic letters and numbers'
        else:
            return 'FAILED: Username must be 8 to 20 alphabetic letters and numbers'
    else:
        return 'FAILED: Username is already taken'


def get_registered_user(username):
    return RegisteredUsers.get_user(username)


def edit_password(user):
    if user.username == 'System':
        return "FAILED: System Can't changed password"
    status = RegisteredUsers.get_user(user.username)
    if status and user.username is not None and user.password is not None:
        if re.match(r'[A-Za-z0-9]{8,20}', user.password):
            user.password = hashlib.sha256(user.password.encode()).hexdigest()
            if RegisteredUsers.edit_user_password(user):
                return 'SUCCESS'
            return 'FAILED'
        return 'FAILED: Password must be 8 to 20 alphabetic letters and numbers'
    return "FAILED: username not exists"


def login(user):
    if SystemManagers.login(user.username, hashlib.sha256(user.password.encode()).hexdigest()):
        return "SUCCESS"
    if user.username is not None and user.password is not None:
        if RegisteredUsers.is_user_exists(user.username):
            user.password = hashlib.sha256(user.password.encode()).hexdigest()
            if RegisteredUsers.login(user):
                return "SUCCESS"
            return "FAILED:Password in incorrect"
        return "FAILED: Username is incorrect"
    return "FAILED: Missing Parameters"


# @username wants to remove the user @registered_user and if he is the last owner - delete the shop as well !
def remove_user(username, registered_user):
    if username is not None and registered_user is not None:
        if SystemManagers.is_system_manager(username) is not False:
            sys_manager = SystemManagers.is_system_manager(registered_user.username)
            is_store_manager = StoreManagers.is_store_manager(registered_user.username)
            is_owner = Owners.is_owner(registered_user.username)
            if sys_manager is False:
                user = RegisteredUsers.get_user(registered_user.username)
                if user is not False:
                    result_delete = True
                    if is_store_manager is not False:
                        result_delete = StoreManagers.remove_manager(registered_user.username)
                    else:
                        if is_owner is not False:
                            result_delete = Owners.remove_owner(registered_user.username)
                    return result_delete and RegisteredUsers.remove_user(registered_user.username)
            return False
    return False


def get_purchase_history(username):
    if username is not None:
        return RegisteredUsers.get_purchase_history(username)


def update_details(username, state, age, sex):
    if 0 < int(age) < 120:
        if sex == 'Male' or sex == 'Female':
            if UserDetails.update(username, state, age, sex):
                return "SUCCESS"
            else:
                return "FAILED"
        else:
            return "FAILED: sex must be Male or Female"
    else:
        return "FAILED: age is invalid"


# _____
#   / ___ \
#  | |   | | _ _ _  ____    ____   ____   ___
#  | |   | || | | ||  _ \  / _  ) / ___) /___)
#  | |___| || | | || | | |( (/ / | |    |___ |
#   \_____/  \____||_| |_| \____)|_|    (___/
#

def add_owner(username, owner):
    if username is not None:
        if Owners.get_owner(username, owner.shop_name) is not False:
            if RegisteredUsers.get_user(owner.username) is not False:
                if Owners.get_owner(owner.username, owner.shop_name) is not False:
                    to_return = 'FAILED! ' + owner.username + ' is already an owner'
                    return to_return
                result = Owners.add_owner(owner)
                if result:
                    result = HistoryAppointings.add_history_appointing(username, owner.username, 'Owner', owner.shop_name, strftime("%d-%m-%Y %H:%M:%S", gmtime()), 'Owner')
                else:
                    return "FAILED"
                if result and is_manager_of_shop(owner.username, owner.shop_name):
                    result = remove_store_manager(username, owner.shop_name, owner.username)
                    if result:
                        return "SUCCESS"
                    else:
                        return "FAILED"
                elif result:
                    return "SUCCESS"
                else:
                    return "FAILED"
            else:
                return "FAILED: Username does not exists"
        else:
            return "FAILED: You are not the owner of this shop"
    else:
        return "FAILED: Missing Parameters"


'''def get_permissions(store_manager):
        permission_string = ''
        if store_manager.permission_add_item == 1:'''


def add_manager(username, store_manager):
    if username is not None:
        if Owners.get_owner(username, store_manager.store_name) is not False:
            if RegisteredUsers.get_user(store_manager.username) is not False:
                if store_manager.store_name is not None:
                    if Owners.get_owner(store_manager.username, store_manager.store_name):
                        return "FAILED! An owner can't be store manager"
                    if StoreManagers.add_manager(store_manager):
                        if HistoryAppointings.add_history_appointing(username, store_manager.username, 'Store Manager',
                                                                     store_manager.store_name, strftime("%d-%m-%Y %H:%M:%S", gmtime()), ''):
                            return 'SUCCESS'
                        return "FAILED"
                    return "FAILED"
                else:
                    return "FAILED: Shop does not exists"
            else:
                return "FAILED: User does not exists"
        else:
            return "FAILED: You are not the owner of this shop"
    else:
        return "FAILED: Missing Parameters"


def close_shop(username, shop_name):
    owner_of_shop = Owners.get_owner(username, shop_name)
    if owner_of_shop is not False:
        return Shops.close_shop(shop_name)
    else:
        return False


def re_open_shop(username, shop_name):
    owner_of_shop = Owners.get_owner(username, shop_name)
    if owner_of_shop is not False:
        return Shops.re_open_shop(shop_name)
    else:
        return False


def modify_notifications(owner_username, should_notify):
    return Owners.modify_notifications(owner_username, should_notify)


def add_system_manager(system_manager):
    if system_manager.username == 'System':
        return False
    if RegisteredUsers.get_user(system_manager.username) is False and Shops.search_shop(
            system_manager.username) is False:
        return SystemManagers.add_system_manager(system_manager)


def add_visible_discount(disc, username):
    if disc is not None and username is not None and disc.percentage >= 0:
        is_owner = Owners.get_owner(username, disc.shop_name)
        is_store = Owners.get_owner(username, disc.shop_name)
        if is_owner is not False or is_store is not False:
            return Discount.add_visible_discount(disc)
    return False


def add_invisible_discount(disc, username):
    if disc is not None and username is not None and disc.percentage >= 0:
        is_owner = Owners.get_owner(username, disc.shop_name)
        is_store = Owners.get_owner(username, disc.shop_name)
        if is_owner is not False or is_store is not False:
            return Discount.add_invisible_discount(disc)
    return False


def get_visible_discount(item_id, shop_name):
    if item_id is not None and shop_name is not None:
        return Discount.get_visible_discount(item_id, shop_name)
    return False


def get_invisible_discount(item_id, shop_name, text):
    if item_id is not None and shop_name is not None and text is not None:
        return Discount.get_invisible_discount(item_id, shop_name, text)
    return False


def get_owned_shops(username):
    return Owners.get_shops_by_owner(username)


def is_owner_of_shop(username, shop_name):
    results = get_owned_shops(username)
    for owner in results:
        if owner.shop_name == shop_name:
            return True
    return False


def get_managed_shops(username):
    return StoreManagers.get_manager_shops(username)


def is_owner_on_shop(username, shop_name):
    return Owners.is_owner_on_shop(username, shop_name)


def remove_store_manager(username, shop_name, target_id):
    if Owners.is_owner_on_shop(username, shop_name) is not False:
        return StoreManagers.remove_manager_from_shop(target_id, shop_name)
    return False


def update_permissions(username, store_manager):
    if Owners.is_owner_on_shop(username, store_manager.store_name) is not False:
        previous_store_manager = StoreManagers.get_store_manager(store_manager.username, store_manager.store_name)
        status = StoreManagers.update_permissions(store_manager)
        if status:
            if isEmptyPermissions(previous_store_manager):
                status = HistoryAppointings.update_history_appointing(username, store_manager.username, store_manager.store_name, getPermissionsString(store_manager))
        return status
    return False


def isEmptyPermissions(previous_store_manager):
    cond = previous_store_manager.permission_add_item == 0
    cond = cond and previous_store_manager.permission_edit_item == 0
    cond = cond and previous_store_manager.permission_get_all_messages == 0
    cond = cond and previous_store_manager.permission_get_purchased_history == 0
    cond = cond and previous_store_manager.permission_reply_messages == 0
    cond = cond and previous_store_manager.permission_remove_item == 0
    cond = cond and previous_store_manager.discount_permission == 0
    return cond


def getPermissionsString(store_manager):
    perm_str = ''
    if store_manager.permission_add_item == '1':
        if perm_str != '':
            perm_str += ','
        perm_str += 'adding item'
    if store_manager.permission_edit_item == '1':
        if perm_str != '':
            perm_str += ','
        perm_str += 'editing item'
    if store_manager.permission_get_all_messages == '1':
        if perm_str != '':
            perm_str += ','
        perm_str += 'getting all messages'
    if store_manager.permission_get_purchased_history == '1':
        if perm_str != '':
            perm_str += ','
        perm_str += 'getting purchase history'
    if store_manager.permission_reply_messages == '1':
        if perm_str != '':
            perm_str += ','
        perm_str += 'replying messages'
    if store_manager.permission_remove_item == '1':
        if perm_str != '':
            perm_str += ','
        perm_str += 'removing item'
    if store_manager.discount_permission == '1':
        if perm_str != '':
            perm_str += ','
        perm_str += 'discounting item'
    return perm_str


def is_system_manager(username):
    return SystemManagers.is_system_manager(username)


def get_all_users():
    return RegisteredUsers.get_all_users()


def is_manager_of_shop(username, shop_name):
    return StoreManagers.is_store_manager_of_shop(username, shop_name)


def get_manager(username, shop_name):
    return StoreManagers.get_store_manager(username, shop_name)


def get_user_details(username):
    return UserDetails.get(username)