from DatabaseLayer.getConn import commit_command, select_command
from SharedClasses.Message import Message


def fetch_messages(results):
    array = []
    for item in results:
        array.append(Message(item[0], item[1], item[2], item[3]))
    return array


def fetch_message(result):
    if len(result) == 0:
        return False
    result = result[0]
    return Message(result[0], result[1], result[2], result[3])


def send_message(message):
    sql_query = """
                INSERT INTO Messages (MessageFrom, MessageTo, Content)  
                VALUES ('{}', '{}', '{}');
              """.format(message.from_username, message.to_username, message.content)
    return commit_command(sql_query)


def get_all_messages(actor_id):
    sql_query = """
                SELECT *
                FROM Messages
                WHERE MessageTo = '{}'
              """.format(actor_id)
    return fetch_messages(select_command(sql_query))


def get_all_shop_messages(shop_name):
    sql_query = """
                SELECT *
                FROM Messages
                WHERE MessageTo = '{}'
              """.format(shop_name)
    return fetch_messages(select_command(sql_query))


def send_message_from_shop(message):
    sql_query = """
                  INSERT INTO Messages (MessageFrom, MessageTo, Content)  
                  VALUES ('{}', '{}', '{}')
                  """.format(message.from_username, message.to_username, message.content)
    return commit_command(sql_query)


def get_all_sent_messages(username):
    sql_query = """
                    SELECT *
                    FROM Messages
                    WHERE MessageFrom = '{}'
                  """.format(username)
    return fetch_messages(select_command(sql_query))


def get_all_sent_shop_messages(shop_name):
    sql_query = """
                    SELECT *
                    FROM Messages
                    WHERE MessageFrom = '{}'
                  """.format(shop_name)
    return fetch_messages(select_command(sql_query))
