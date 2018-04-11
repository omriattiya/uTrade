from DatabaseLayer.getConn import commit_command, select_command


def send_message(message_from, message_to, content):
    sql_query = """
                INSERT INTO Messages (MessageFrom, MessageTo, Content)  
                VALUES ('{}', '{}', '{}');
              """.format(message_from, message_to, content)
    return commit_command(sql_query)


def get_all_messages(actor_id):
    sql_query = """
                SELECT *
                FROM Messages
                WHERE MessageTo = '{}'
              """.format(actor_id)
    return select_command(sql_query)


def get_all_shop_messages(shop_name):
    sql_query = """
                SELECT *
                FROM Messages
                WHERE MessageTo = '{}'
              """.format(shop_name)
    return select_command(sql_query)


def send_message_from_shop(message, shop_name, to):
    sql_query = """
                  INSERT INTO Messages (MessageFrom, MessageTo, Content)  
                  VALUES ('{}', '{}', '{}')
                  """.format(shop_name, to, message)
    return commit_command(sql_query)
