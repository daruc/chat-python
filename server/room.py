class Room:

    def __init__(self):
        self._messages = []

    def add_message(self, author, message):
        self._messages.append((author, message))

    def messages_to_string(self):
        return ''.join((aut + ': ' + msg + '\n') for aut, msg in self._messages)
