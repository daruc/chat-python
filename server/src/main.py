import http.server
import socketserver
import re
from room import Room
from resources import ConfigRegister
import argparse

# server options
argparser = argparse.ArgumentParser(description='Chat server')
argparser.add_argument('--port', type=int)
argparser.add_argument('--rooms', type=str, nargs='+')
args = argparser.parse_args()

config_register = ConfigRegister.get_instance()

if args.port:
    global PORT
    PORT = args.port
else:
    PORT = int(config_register['port'])

if args.rooms:
    global rooms_number
    global rooms
    rooms_number = len(args.rooms)
    rooms = [Room(room_name) for room_name in args.rooms]
    print(rooms)
else:
    rooms_number = int(config_register['rooms_number'])
    rooms = []
    for room_number in range(1, rooms_number + 1):
        room_name = config_register['room_name#' + str(room_number)]
        room = Room(room_name)
        rooms.append(room)


def get_room(n_rooms):
    """Returns room object by number from 1"""
    return rooms[int(n_rooms) - 1]


class RequestHandler(http.server.BaseHTTPRequestHandler):

    rooms_list_pattern = re.compile(r'^/rooms$')
    room_pattern = re.compile(r'^/room/+$')

    def do_GET(self):
        get_method = self._choose_get_method()
        get_method()
        print('get: ' + self.path)

    def _get_messages(self):
        print('get_messages()')
        match_obj = re.match(r'.*/rooms/(.*)', self.path)
        n_room = match_obj.group(1)
        print(n_room)
        source_room = get_room(n_room)
        all_messages = source_room.messages_to_string()
        all_messages_encoded = all_messages.encode('utf-8')

        self.send_response(200)
        self.send_header('Content-Length', len(all_messages_encoded))
        self.end_headers()
        self.wfile.write(all_messages_encoded)

    def _get_rooms(self):
        print('get_rooms')
        rooms_str = '\n'.join(r.get_name() for r in rooms)
        rooms_str = rooms_str.encode('utf-8')

        self.send_response(200)
        self.send_header('Content-Length', len(rooms_str))
        self.end_headers()
        self.wfile.write(rooms_str)

    def _choose_get_method(self):
        """Returns appropriate method which have to serve request by given path."""

        if re.search(r'^/rooms$', self.path):
            return self._get_rooms
        elif re.search(r'^/rooms/.+$', self.path):
            return self._get_messages

    def do_POST(self):
        """Adds new message to appropriate room."""

        data_length = int(self.headers['Content-Length'])
        nickname_length = int(self.headers['Nickname-Length'])
        message_length = data_length - nickname_length

        nickname = self.rfile.read(nickname_length)
        nickname = nickname.decode('utf-8')
        print(nickname)

        message = self.rfile.read(message_length)
        message = message.decode('utf-8')
        print(message)

        match_obj = re.match(r'^/rooms/(.+)$', self.path)
        destination_room = get_room(match_obj.group(1))
        destination_room.add_message(nickname, message)

        self.send_response(200)
        self.end_headers()
        print('post')


with socketserver.TCPServer(('', PORT), RequestHandler) as httpd:
    print('Serving at port ', PORT)
    httpd.serve_forever()   # Server's main loop
