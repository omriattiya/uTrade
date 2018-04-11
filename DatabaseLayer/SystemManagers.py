from DatabaseLayer.getConn import commit_command


def is_system_manager(username):
    sql = """
                SELECT *
                FROM SystemManagers
                WHERE username = '{}'
            """.format(username)
    return commit_command(sql)


def add_system_manager(username):
    sql = """
                INSERT INTO SystemManagers (username)
                VALUES ('{}')
                """.format(username)
    return commit_command(sql)



