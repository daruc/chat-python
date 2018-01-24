import requests
from resources import ConfigRegister


def send(room_number, message):
    config_register = ConfigRegister.get_instance()
    nickname = config_register['nickname']
    nickname_length = len(nickname.encode('utf-8'))
    message_to_send = nickname + message.strip()
    message_encoded = message_to_send.encode('utf-8')

    head = {'Content-Length': str(len(message_encoded)), 'Nickname-Length': str(nickname_length)}
    server_url = ConfigRegister.get_instance()['server_url']
    server_url = server_url + 'rooms/' + str(room_number)
    r = requests.post(server_url, data=message_encoded, headers=head)
    print('send: ' + message + ', status: ' + str(r.status_code))


def get(room_number):
    config_register = ConfigRegister.get_instance()
    server_url = config_register['server_url'] + 'rooms/' + str(room_number)

    r = requests.get(server_url)
    return r.content.decode('utf-8')


def get_rooms():
    config_register = ConfigRegister.get_instance()
    server_url = config_register['server_url'] + 'rooms'

    r = requests.get(server_url)
    return r.content.decode('utf-8').split('\n')
