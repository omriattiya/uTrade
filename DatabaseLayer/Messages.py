from DatabaseLayer.getConn import get_conn


def send_message(message_from, message_to, content):
    c = get_conn().cursor()
    c.execute("""
                INSERT INTO Messages (MessageFrom, MessageTo, Content)  
VALUES ('{}', '{}', '{}');
              """.format(message_from, message_to,
                         content))
    return c.fetchall()


def get_all_messages(id):
    c = get_conn().cursor()
    c.execute("""
                SELECT *
                FROM Messages
                WHERE MessageTo = '{}'
              """.format(id))
    return c.fetchall()