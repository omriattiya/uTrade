import sqlite3

from DatabaseLayer import ShoppingPolicies
from DatabaseLayer import SystemManagers
from DatabaseLayer import Owners

#    ____________________________________   GET ALL     ___________________________________________________


def get_all_shopping_policy_on_shop(shop_name):
    return ShoppingPolicies.get_all_shopping_policy_on_shop(shop_name)


def get_all_shopping_policy_on_items():
    return ShoppingPolicies.get_all_shopping_policy_on_items()


def get_all_shopping_policy_on_category():
    return ShoppingPolicies.get_all_shopping_policy_on_category()


def get_all_shopping_policy_on_identity():
    return ShoppingPolicies.get_all_shopping_policy_on_identity()


#    ____________________________________   INSERT     ___________________________________________________


def add_shopping_policy_on_items(username, item_name, conditions, restrict, quantity):
    if item_name is not None and conditions is not None:
        if restrict is not None and quantity is not None:
            if restrict not in ['N', 'AL', 'E', 'UT']:
                return "FAILED: Invalid value of restrict."
            if int(quantity) < 0:
                return "FAILED: Negative quantity is invalid."
            if SystemManagers.is_system_manager(username) is not False:
                if not ShoppingPolicies.add_shopping_policy_on_items(item_name, conditions, restrict, quantity):
                    return "FAILED: DB error."
                return True
            return 'FAILED: you are not a System Manager'
        return "FAILED: One (or more) of the parameters is None"
    return "FAILED: One (or more) of the parameters is None"


def add_shopping_policy_on_category(username, category, conditions, restrict, quantity):
    if category is not None and conditions is not None:
        if restrict is not None and quantity is not None:
            if restrict not in ['N', 'AL', 'E', 'UT']:
                return "FAILED: Invalid value of restrict."
            if int(quantity) < 0:
                return "FAILED: Negative quantity is invalid."
            if SystemManagers.is_system_manager(username) is not False:
                if not ShoppingPolicies.add_shopping_policy_on_category(category, conditions, restrict, quantity):
                    return "FAILED: DB error."
                return True
            return 'FAILED: you are not a System Manager'
        return "FAILED: One (or more) of the parameters is None"
    return "FAILED: One (or more) of the parameters is None"


def add_shopping_policy_on_shop(username, shop_name, conditions, restrict, quantity):
    if shop_name is not None and conditions is not None:
        if restrict is not None and quantity is not None:
            if restrict not in ['N', 'AL', 'E', 'UT']:
                return "FAILED: Invalid value of restrict."
            if int(quantity) < 0:
                return "FAILED: Negative quantity is invalid."
            if Owners.get_owner(username, shop_name) is not False:
                if not ShoppingPolicies.add_shopping_policy_on_shop(shop_name, conditions, restrict, quantity):
                    return "FAILED: DB error."
                return True
            return 'FAILED: you are not a the Owner of the shop'
        return "FAILED: One (or more) of the parameters is None"
    return "FAILED: One (or more) of the parameters is None"


def add_shopping_policy_on_identity(username, conditions, restrict, quantity):
    if conditions is not None and restrict is not None and quantity is not None:
        if restrict not in ['N', 'AL', 'E', 'UT']:
            return "FAILED: Invalid value of restrict."
        if int(quantity) < 0:
            return "FAILED: Negative quantity is invalid."
        if SystemManagers.is_system_manager(username) is not False:
            if not ShoppingPolicies.add_shopping_policy_on_identity(conditions, restrict, quantity):
                return "FAILED: DB error."
            return True
        return 'FAILED: you are not a System Manager'
    return "FAILED: One (or more) of the parameters is None"


#    ____________________________________   DELETE     ___________________________________________________


def remove_shopping_policy_on_identity(username, policy_id):
    if policy_id is not None and policy_id > 0:
        if SystemManagers.is_system_manager(username) is not False:
            if not ShoppingPolicies.remove_shopping_policy_on_identity(policy_id):
                return "FAILED: DB error."
            return True
        return 'FAILED: you are not a System Manager'
    return "FAILED: Invalid id of Policy"


def remove_shopping_policy_on_shop(username, policy_id, shop_name):
    if policy_id is not None and policy_id > 0:
        if Owners.get_owner(username, shop_name) is not False:
            if not ShoppingPolicies.remove_shopping_policy_on_shop(policy_id):
                return "FAILED: DB error."
            return True
        return 'FAILED: you are not a the Owner of the shop'
    return "FAILED: Invalid id of Policy"


def remove_shopping_policy_on_items(username, policy_id):
    if policy_id is not None and policy_id > 0:
        if SystemManagers.is_system_manager(username) is not False:
            if not ShoppingPolicies.remove_shopping_policy_on_items(policy_id):
                return "FAILED: DB error."
            return True
        return 'FAILED: you are not a System Manager'
    return "FAILED: Invalid id of Policy"


def remove_shopping_policy_on_category(username, policy_id):
    if policy_id is not None and policy_id > 0:
        if SystemManagers.is_system_manager(username) is not False:
            if not ShoppingPolicies.remove_shopping_policy_on_category(policy_id):
                return "FAILED: DB error."
            return True
        return 'FAILED: you are not a System Manager'
    return "FAILED: Invalid id of Policy"


#    ____________________________________   UPDATE     ___________________________________________________


def update_shopping_policy_on_identity(username, policy_id, field_name, new_value):
    if policy_id is not None and field_name is not None and new_value is not None:
        if int(policy_id) < 0:
            return "FAILED: Invalid id of Policy"
        if field_name not in ['conditions', 'restrict', 'quantity']:
            return "FAILED: Invalid field name"
        if SystemManagers.is_system_manager(username) is not False:
            if field_name in ['conditions']:
                status = checkConditionsSyntax(new_value)
                if status is not True:
                    return status

            if not ShoppingPolicies.update_shopping_policy_on_identity(policy_id, field_name, new_value):
                return "FAILED: DB error."
            return True
        return 'FAILED: you are not a System Manager'
    return "FAILED: One (or more) of the parameters is None"


def update_shopping_policy_on_shop(username, policy_id, field_name, new_value, shop_name):
    if policy_id is not None and field_name is not None and new_value is not None:
        if int(policy_id) < 0:
            return "FAILED: Invalid id of Policy"
        if field_name not in ['shop_name', 'conditions', 'restrict', 'quantity']:
            return "FAILED: Invalid field name"
        if Owners.get_owner(username, shop_name) is not False:
            if field_name in ['conditions']:
                status = checkConditionsSyntax(new_value)
                if status is not True:
                    return status

            if not ShoppingPolicies.update_shopping_policy_on_shop(policy_id, field_name, new_value):
                return "FAILED: DB error."
            return True
        return 'FAILED: you are not a the Owner of the shop'
    return "FAILED: One (or more) of the parameters is None"


def update_shopping_policy_on_items(username, policy_id, field_name, new_value):
    if policy_id is not None and field_name is not None and new_value is not None:
        if int(policy_id) < 0:
            return "FAILED: Invalid id of Policy"
        if field_name not in ['item_name', 'conditions', 'restrict', 'quantity']:
            return "FAILED: Invalid field name"
        if SystemManagers.is_system_manager(username) is not False:
            if field_name in ['conditions']:
                status = checkConditionsSyntax(new_value)
                if status is not True:
                    return status

            if not ShoppingPolicies.update_shopping_policy_on_items(policy_id, field_name, new_value):
                return "FAILED: DB error."
            return True
        return 'FAILED: you are not a System Manager'
    return "FAILED: One (or more) of the parameters is None"


def update_shopping_policy_on_category(username, policy_id, field_name, new_value):
    if policy_id is not None and field_name is not None and new_value is not None:
        if int(policy_id) < 0:
            return "FAILED: Invalid id of Policy"
        if field_name not in ['category', 'conditions', 'restrict', 'quantity']:
            return "FAILED: Invalid field name"
        if SystemManagers.is_system_manager(username) is not False:
            if field_name in ['conditions']:
                status = checkConditionsSyntax(new_value)
                if status is not True:
                    return status

            if not ShoppingPolicies.update_shopping_policy_on_category(policy_id, field_name, new_value):
                return "FAILED: DB error."
            return True
        return 'FAILED: you are not a System Manager'
    return "FAILED: One (or more) of the parameters is None"


logic_operators = ['AND', 'OR', 'NOT']
fields = ['age', 'sex', 'state']
numerical_operators = ['>', '<', '=', '>=', '<=', '!=']
genders = ["'Male'", "'Female'"]
# Don't worry I didn't really typed all of these 256 states.
states = ["'AFG'", "'ALA'", "'ALB'", "'DZA'", "'ASM'", "'AND'", "'AGO'", "'AIA'", "'ATA'", "'ATG'", "'ARG'", "'ARM'",
          "'ABW'", "'AUS'", "'AUT'", "'AZE'", "'BHS'", "'BHR'", "'BGD'", "'BRB'", "'BLR'", "'BEL'", "'BLZ'", "'BEN'",
          "'BMU'", "'BTN'", "'BOL'", "'BES'", "'BIH'", "'BWA'", "'BVT'", "'BRA'", "'IOT'", "'BRN'", "'BGR'", "'BFA'",
          "'BDI'", "'KHM'", "'CMR'", "'CAN'", "'CPV'", "'CYM'", "'CAF'", "'TCD'", "'CHL'", "'CHN'", "'CXR'", "'CCK'",
          "'COL'", "'COM'", "'COG'", "'COD'", "'COK'", "'CRI'", "'CIV'", "'HRV'", "'CUB'", "'CUW'", "'CYP'", "'CZE'",
          "'DNK'", "'DJI'", "'DMA'", "'DOM'", "'ECU'", "'EGY'", "'SLV'", "'GNQ'", "'ERI'", "'EST'", "'ETH'", "'FLK'",
          "'FRO'", "'FJI'", "'FIN'", "'FRA'", "'GUF'", "'PYF'", "'ATF'", "'GAB'", "'GMB'", "'GEO'", "'DEU'", "'GHA'",
          "'GIB'", "'GRC'", "'GRL'", "'GRD'", "'GLP'", "'GUM'", "'GTM'", "'GGY'", "'GIN'", "'GNB'", "'GUY'", "'HTI'",
          "'HMD'", "'VAT'", "'HND'", "'HKG'", "'HUN'", "'ISL'", "'IND'", "'IDN'", "'IRN'", "'IRQ'", "'IRL'", "'IMN'",
          "'ISR'", "'ITA'", "'JAM'", "'JPN'", "'JEY'", "'JOR'", "'KAZ'", "'KEN'", "'KIR'", "'PRK'", "'KOR'", "'KWT'",
          "'KGZ'", "'LAO'", "'LVA'", "'LBN'", "'LSO'", "'LBR'", "'LBY'", "'LIE'", "'LTU'", "'LUX'", "'MAC'", "'MKD'",
          "'MDG'", "'MWI'", "'MYS'", "'MDV'", "'MLI'", "'MLT'", "'MHL'", "'MTQ'", "'MRT'", "'MUS'", "'MYT'", "'MEX'",
          "'FSM'", "'MDA'", "'MCO'", "'MNG'", "'MNE'", "'MSR'", "'MAR'", "'MOZ'", "'MMR'", "'NAM'", "'NRU'", "'NPL'",
          "'NLD'", "'NCL'", "'NZL'", "'NIC'", "'NER'", "'NGA'", "'NIU'", "'NFK'", "'MNP'", "'NOR'", "'OMN'", "'PAK'",
          "'PLW'", "'PSE'", "'PAN'", "'PNG'", "'PRY'", "'PER'", "'PHL'", "'PCN'", "'POL'", "'PRT'", "'PRI'", "'QAT'",
          "'REU'", "'ROU'", "'RUS'", "'RWA'", "'BLM'", "'SHN'", "'KNA'", "'LCA'", "'MAF'", "'SPM'", "'VCT'", "'WSM'",
          "'SMR'", "'STP'", "'SAU'", "'SEN'", "'SRB'", "'SYC'", "'SLE'", "'SGP'", "'SXM'", "'SVK'", "'SVN'", "'SLB'",
          "'SOM'", "'ZAF'", "'SGS'", "'SSD'", "'ESP'", "'LKA'", "'SDN'", "'SUR'", "'SJM'", "'SWZ'", "'SWE'", "'CHE'",
          "'SYR'", "'TWN'", "'TJK'", "'TZA'", "'THA'", "'TLS'", "'TGO'", "'TKL'", "'TON'", "'TTO'", "'TUN'", "'TUR'",
          "'TKM'", "'TCA'", "'TUV'", "'UGA'", "'UKR'", "'ARE'", "'GBR'", "'USA'", "'UMI'", "'URY'", "'UZB'", "'VUT'",
          "'VEN'", "'VNM'", "'VGB'", "'VIR'", "'WLF'", "'ESH'", "'YEM'", "'ZMB'", "'ZWE'"]


def checkConditionsSyntax(conditions):
    # WHAT I'M DOING HERE IS DUMB IN SO MANY WAYS. DON'T EVER DO THAT
    replaced_conditions = conditions.replace("''", "'")
    without_parentheses_conditions = replaced_conditions.replace("(", "")
    without_parentheses_conditions = without_parentheses_conditions.replace(")", "")

    # First checking that there are only valid values
    tokens = without_parentheses_conditions.split()
    for token in tokens:
        if token not in logic_operators and \
                        token not in fields and \
                        token not in numerical_operators \
                and token not in genders and \
                        token not in states:
            try:
                token = int(token)
                if (token > 100 or token < 0):
                    return "FAILED: " + str(token) + " is out of range"
                else:
                    continue
            except:
                return "FAILED unrecognized token " + token

    # Checking sql syntax is correct.
    try:
        conn = sqlite3.connect('./checking_syntax')
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS UserDetails(
                                      username CHAR(30), 
                                      state CHAR(30) DEFAULT NULL,
                                      age INTEGER DEFAULT NULL,
                                      sex INTEGER DEFAULT NULL,
                                      PRIMARY KEY(username)
                                    )""")
        c.execute("""SELECT *
                    FROM UserDetails
                    WHERE {}""".format(replaced_conditions))
        conn.close()
    except sqlite3.Error as e:
        return "FAILED: {}".format(e)
    return True
