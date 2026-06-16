# client
import socket
import sys
from libs import add_header
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    s.connect((socket.gethostname(),4444))
except Exception as e:
    print("server is down")
    sys.exit()
HEADERSIZE = 10
def receive_msg(sock):
    full_msg = ""
    new_msg = True
    msg_len = 0

    while True:
        msg = sock.recv(2048)
        msg_decoded = msg.decode("utf-8")

        if not msg:
            break

        if new_msg:
            msg_len = int(msg_decoded[:HEADERSIZE])    
            new_msg = False

        full_msg += msg_decoded


        if len(full_msg) - HEADERSIZE == msg_len:
            return full_msg[HEADERSIZE:]


welcome = receive_msg(s)
print (welcome)
for w in range(1):
    cmd = input()
    if cmd == "close" or not cmd:
        break

    
    s.send(cmd.encode("utf-8"))


    reply = receive_msg(s)
    if not reply:
        print("server is down")
        break
    
    print(reply)
    break
while True:
    cmd = input("""┌──(root㉿root-kali)-[~]
└─# """) #خليتها root㉿root-kali مؤقتا لحد ما اعمل users
    if cmd == "close" or not cmd:
        break

    s.send(cmd.encode("utf-8"))


    reply = receive_msg(s)
    if not reply:
        print("server is down")
        break
    
    print(reply)