# server
import socket
import subprocess
import os
import libs
import auth

HEADERSIZE = 10

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((socket.gethostname() , 4444))



s.listen(5)

while True:
    clientsocket , address = s.accept()
    print(f"Connection from {address}")


    login_1 = auth.login(clientsocket,address[0])
    if login_1 == False :
        clientsocket.close()
        continue
    elif login_1 == "wrong":
        clientsocket.close()
        continue


    print(f"{address} are good human")

    
    while True:
        try:

            cmd = clientsocket.recv(1024).decode("utf-8")
        
            if not cmd or cmd == "close":
                clientsocket.close()
                break

            elif cmd.startswith("cd "):
                try:
                    path = cmd[3:].strip()
                    os.chdir(path)
                    reply = os.getcwd()
                except Exception as e:
                    reply = f"ERROR: {str(e)}"
                


            try:
                reply = subprocess.check_output(cmd,shell=True,stderr=subprocess.STDOUT).decode("utf-8")
                if not reply:
                    reply = "Command executed successfully with no output."

            except Exception as e:
                reply = f"ERROR: {str(e)}"
                
                
            full_reply = libs.add_header(reply)

            libs.send(clientsocket,full_reply)    
        
        
        
        
        except Exception:
            print(f"DONE EXPELLED : {clientsocket}")
            clientsocket.close()
            break