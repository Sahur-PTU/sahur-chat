import socketserver
WRITE = 'chat.txt'

class server(socketserver.ThreadingTCPServer):
    allow_reuse_address=True
class Handler(socketserver.StreamRequestHandler):
    def handle(self):
        with open(WRITE, 'ab') as f:
         while True:
             write = self.rfile.readlines()
             if not write:
                 break
def start_server():
    serverd = server(('127.0.0.1', 8000),RequestHandlerClass=False)
    serverd.serve_forever()
start_server()