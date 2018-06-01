from DatabaseLayer.getConn import commit_command, select_command


def parse_user_details(results):
    if len(results) == 0:
        return False
    result = results[0]
    return {'username': result[0],
            'state': result[1],
            'age': result[2],
            'sex': result[3]}


def insert(username):
    sql_query = """
                    INSERT INTO UserDetails (username)
                    VALUES ('{}')
                    """.format(username)
    return commit_command(sql_query)


def update(username, state, age, sex):
    sql_query = """
                UPDATE UserDetails
                SET state = '{}',age = '{}', sex = '{}'
                WHERE username = '{}'
                """.format(state, age, sex, username)
    return commit_command(sql_query)


def get(username):
    sql_query = """
                    SELECT *
                    FROM UserDetails
                    WHERE username = '{}'
                  """.format(username)
    return parse_user_details(select_command(sql_query))


def is_meet_conditions(username, conditions):
    sql_query = """
                    SELECT *
                    FROM UserDetails
                    WHERE username = '{}' AND '{}'
                      """.format(username, conditions)
    return parse_user_details(select_command(sql_query))
