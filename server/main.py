import http.server
import socketserver
from room import Room

PORT = 8080
room = Room()


class RequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        all_messages = room.messages_to_string()
        all_messages_encoded = all_messages.encode('UTF-8')

        self.send_response(200)
        self.send_header('Content-Length', len(all_messages_encoded))
        self.end_headers()
        self.wfile.write(all_messages_encoded)
        print('get')

    def do_POST(self):
        data_length = int(self.headers['Content-Length'])
        nickname_length = int(self.headers['Nickname-Length'])
        message_length = data_length - nickname_length

        nickname = self.rfile.read(nickname_length)
        nickname = nickname.decode('UTF-8')
        print(nickname)

        message = self.rfile.read(message_length)
        message = message.decode('UTF-8')
        print(message)

        room.add_message(nickname, message)

        self.send_response(200)
        self.end_headers()
        print('post')


with socketserver.TCPServer(('', PORT), RequestHandler) as httpd:
    print('Serving at port ', PORT)
    httpd.serve_forever()