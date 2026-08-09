# client
import socket
import sys
import libs 


try:

    def recvClientSide(s):
        while True:
            l = 0
            import time
            time.sleep(1)
            welcome = libs.receive_msg(s)
            if welcome:
                if welcome["action"] == "close":
                    print(welcome["user_msg"])
                    sys.exit()
                elif welcome["action"] == "SENDED?":
                    print(welcome["user_msg"])
                    a = libs.ready(action="YES")
                    libs.send(s,a)
                    l = 0
                    continue
                else:
                    return welcome
                break

        
            else:
                
                # print("hone")
                # sys.exit()
                while True:
                    time.sleep(1)    
                    l+=1
                    print(l)
                    welcome = libs.receive_msg(s)
                    print(welcome["user_msg"])
                    if welcome["action"] == "SENDED?":
                        a = libs.ready(action="YES")
                        libs.send(s,a)
                        print("yes")
                        l = 0
                        continue
                    elif welcome:
                        return welcome
                    if l >= 10:
                        print("server is down")
                        sys.exit()

    #-------------------------





    location = False
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        s.connect((socket.gethostname(),4444))
    except Exception as e:
        print("server is down")
        sys.exit()
    while True:
        welcome = recvClientSide(s)
        if welcome["action"] == "TRUE_GO":
            print(welcome["user_msg"])
            r = True
            if welcome["hint"] == "location":
                location = welcome["action"] 
            break
        else:
            if welcome["action"] == "BLOCKED":
                print(welcome["user_msg"])
                sys.exit()
            print(welcome["user_msg"])
            cmd = input()
            if cmd == "close" or not cmd:
                sys.exit()
                break
            cmd = libs.ready(user_msg=cmd)
            libs.send(s,cmd)
    user_name = welcome["user_name"]
    while r == True:
        if location:
            cmd = input(f"""┌──({user_name}㉿root-kali)-[{location}]
└─# """)
        else:
            cmd = input(f"""┌──({user_name}㉿root-kali)-[~]
└─# """)
        if cmd == "close" or not cmd:
            break
        f = libs.ready(user_msg=cmd)
        libs.send(s,f)


        reply = recvClientSide(s)
        if not reply:
            print("server is down")
            break
        if reply["hint"] == "location":
            location = reply["action"] 

        print(reply["user_msg"])
except Exception as error:
    print(f"ERROR : {error}")