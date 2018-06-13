class EventTuple:
    def __init__(self, username, time, event):
        self.username = username
        self.time = time
        self.event = event


class ErrorTuple:
    def __init__(self, username, time, event, additional_details):
        self.additional_details = additional_details
        self.username = username
        self.time = time
        self.event = event


class LoginTuple:
    def __init__(self, username, time):
        self.username = username
        self.time = time
