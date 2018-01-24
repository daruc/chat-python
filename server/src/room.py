class Room:

    def __init__(self, name):
        self._messages = []
        self._name = name

    def add_message(self, author, message):
        self._messages.append((author, message))

    def messages_to_string(self):
        return ''.join((aut + ': ' + msg + '\n') for aut, msg in self._messages)

    def get_name(self):
        return self._name
