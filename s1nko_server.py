import socketserver,ipaddress
WRITE = 'chat.txt'
Ip = None
Port = None

print("sahur-chat server setup")
def settingip():
    global Ip
    while True:
     Ip = input(str("Server IP:\n>"))
     try:
            ipaddress.IPv4Address(Ip)
     except ipaddress.AddressValueError:
            print("Wrong IPv4 address. For example: XXX.XXX.XXX.XXX.XXX")
            settingip()
     print("Server ip",Ip,"is right?[y/n]")
     checkip=input(">")
     if checkip=="y" or checkip=="" or checkip=="ю" or checkip=="Ю" or checkip=="Y":
       settingport()
     else:
      settingip()
def settingport():
    global Port
    Port=int(input("Server Port:\n>"))
    if not 1 <= Port <= 65535:
        print("The port should be from 1 to 65535")
        settingport()
    print("Server port:",Port,"is right?[y/n]")
    checkport=input(">")
    if checkport=="y" or checkport=="" or checkport=="ю" or checkport=="Ю" or checkport=="Y":
        start_server()
    else:
     settingport()
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
    print("Server starts on",Ip,":",Port)
    serverd = server((Ip, Port),Handler)
    serverd.serve_forever()
settingip()