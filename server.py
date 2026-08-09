# server
import socket
import subprocess
import os
import libs
import auth
try:

    HEADERSIZE = 10

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((socket.gethostname() , 4444))



    s.listen(5)

    while True:
        clientsocket , address = s.accept()
        print(f"Connection from {address}")


        login_1 = auth.login(clientsocket,address[0])
        if login_1 == False or login_1 == "wrong":
            clientsocket.close()
            continue


        print(f"{address[0]} DONE LOGIN")

        i = True
        while True:
            try:

                cmd_recv = libs.receive_msg(clientsocket)
                cmd = cmd_recv["user_msg"]
                if not cmd or cmd == "close":
                    clientsocket.close()
                    break

                elif cmd.startswith("cd "):
                    try:
                        path = cmd[3:].strip()
                        os.chdir(path)
                        reply = os.getcwd()
                        full_reply=libs.ready(user_msg=reply,action=reply,hint="location")
                

                        libs.send(clientsocket,full_reply)
                        continue
                    except Exception as e:
                        reply = f"ERROR: {str(e)}"
                else:
                    


                    try:
                        reply = subprocess.check_output(cmd,shell=True,stderr=subprocess.STDOUT).decode("utf-8")
                        if not reply:
                            reply = "Command executed successfully with no output."

                    except Exception as e:
                        reply = f"ERROR: {str(e)}"
                    
                if i == True:
                    ac = os.getcwd()
                    full_reply=libs.ready(user_msg=reply,action=ac,hint="location")
                

                    libs.send(clientsocket,full_reply)
                    i = False        
                    continue
                full_reply=libs.ready(user_msg=reply)
                

                libs.send(clientsocket,full_reply)    
            
            
            
            
            except Exception:
                print(f"DONE EXPELLED : {address}")
                clientsocket.close()
                break
except Exception as ERROR:
    print(f"ERROR : {ERROR}")