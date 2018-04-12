from DatabaseLayer.getConn import commit_command, select_command


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
