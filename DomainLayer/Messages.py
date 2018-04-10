from DatabaseLayer import Messages


def send_message(message_from, message_to, content):
    if message_from is not None and message_to is not None and content is not None:
        return Messages.send_message(message_from, message_to, content)


def get_all_messages(id):
    if id is not None:
        return Messages.get_all_messages(id)
