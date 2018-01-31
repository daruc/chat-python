"""Module response for communication with server."""

import requests
from resources import ConfigRegister


def send(room_number, message):
    """Sends message to room."""

    config_register = ConfigRegister.get_instance()
    nickname = config_register['nickname']
    nickname_length = len(nickname.encode('utf-8'))
    message_to_send = nickname + message.strip()
    message_encoded = message_to_send.encode('utf-8')

    head = {'Content-Length': str(len(message_encoded)), 'Nickname-Length': str(nickname_length)}
    server_url = ConfigRegister.get_instance()['server_url']
    server_url = server_url + 'rooms/' + str(room_number)
    requests.post(server_url, data=message_encoded, headers=head)


def get(room_number):
    """Gets chat from server."""

    config_register = ConfigRegister.get_instance()
    server_url = config_register['server_url'] + 'rooms/' + str(room_number)

    request = requests.get(server_url)
    return request.content.decode('utf-8')


def get_rooms():
    """Returns list of available rooms on the server."""

    config_register = ConfigRegister.get_instance()
    server_url = config_register['server_url'] + 'rooms'

    request = requests.get(server_url)
    return request.content.decode('utf-8').split('\n')
