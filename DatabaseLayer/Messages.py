from DatabaseLayer.getConn import getConn


def send_message(message_from, message_to, content):
    c = getConn().cursor()
    c.execute("""
                INSERT INTO Messages (MessageFrom, MessageTo, Content)  
VALUES ({}, {}, {});
              """.format(message_from, message_to,
                         content))
    return c.fetchall()


def get_all_messages(id):
    c = getConn().cursor()
    c.execute("""
                SELECT *
                FROM Messages
                WHERE MessageTo = {}
              """.format(id))
    return c.fetchall()