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


def get_all_shop_messages(shop_name):
    # TODO: tomer -> notice that in the 'messages'
    # TODO:         table the fields 'MessageFrom' and 'MessageTo'
    # TODO:         are both char(30) and here you are getting an Integer

    return True


def send_message_from_shop(message, shop_name, to):
    # TODO: tomer -> notice that in the 'messages'
    # TODO:         table the fields 'MessageFrom' and 'MessageTo'
    # TODO:         are both char(30) and here you are getting an Integer

    # TODO: also the 'to' parameter can be a shop_name or a username

    return True
