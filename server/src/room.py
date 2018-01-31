"""Module manage users interactions inside chat room."""


class Room:
    """Represents chat room."""

    def __init__(self, name):
        self._messages = []
        self._name = name

    def add_message(self, author, message):
        """Adds new message"""

        self._messages.append((author, message))

    def messages_to_string(self):
        """Converts lists of authors and messages to joined string."""

        return ''.join((aut + ': ' + msg + '\n') for aut, msg in self._messages)

    def get_name(self):
        """Return name of the room."""

        return self._name
