from DatabaseLayer.getConn import commit_command, select_command
from SharedClasses.SystemManager import SystemManager


def parse_system_managers(system_managers):
    system_managers_list = []
    for system_manager in system_managers:
        system_managers_list.append(SystemManager(system_manager[0], system_manager[1]))
    return system_managers_list


def is_system_manager(username):
    sql_query = """
                SELECT *
                FROM SystemManagers
                WHERE username = '{}'
            """.format(username)
    results = select_command(sql_query)
    return len(results) == 1


def add_system_manager(username, password):
    sql_query = """
                INSERT INTO SystemManagers (username, password)
                VALUES ('{}', '{}')
                """.format(username, password)
    return commit_command(sql_query)
