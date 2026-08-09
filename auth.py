# auth
import libs , json


black_list = []
failed_attemps = {}

def login(client_socket,client_ip):
    try:
        mac = libs.get_client_mac(client_ip)


        try:
            with open("data.json","r") as f:
                my_dicit = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            my_dict = {"start": "start"}
            with open("data.json", "w") as f:
                json.dump(my_dict, f, indent=4)

            with open("data.json","r") as f:
                my_dicit = json.load(f)


        my_dicit["KERNEL"] = {"pass" : "kernel","role" : "admin"}
        with open("data.json","w") as f:
            json.dump(my_dicit,f,indent=4)

        

        
        while True:
            if mac in black_list:
                print(f"The {client_ip} was BLOCKED")
                fail_msg = libs.ready(action="BLOCKED",user_msg="YOU ARE BLOCKED BY MAC")
                    
                libs.send(client_socket,fail_msg)
                return False

            msg_log = libs.ready(user_msg="LOGIN OR LOGUP")
            libs.send(client_socket,msg_log)
            recv_log = libs.receive_msg(client_socket)
    # 
            if recv_log["user_msg"].lower() == "login":

                msg = libs.ready(user_msg="USER NAME")
                libs.send(client_socket,msg)
                client_user = libs.receive_msg(client_socket)

                msg = libs.ready(user_msg="PASSWORD")
                libs.send(client_socket,msg)
                client_pass = libs.receive_msg(client_socket)

                r = True
                client_data = my_dicit.get(client_user["user_msg"],"NONE")
                while True:
                    
                    if client_data == "NONE":
                        try:
                            if failed_attemps[mac] == 2:
                                failed_attemps[mac] +=  1
                                fail_msg = libs.ready(action="BLOCKED",user_msg="YOU ARE BLOCKED BY MAC")
                                libs.send(client_socket,fail_msg)
                                return False
                        except:
                            pass

                        r = False
                        reply = libs.ready(user_msg="WRONG USERNAME,TRY LOGUP",action="SENDED?")
                        libs.send(client_socket,reply)
                        client_DONE = libs.receive_msg(client_socket)
                        if client_DONE["action"] == "YES":
                            if mac not in failed_attemps:
                                failed_attemps[mac] = 1
                                
                            else:
                                failed_attemps[mac] +=  1
                            break
                        else:
                            print("error")
                        




                            print(f"{client_ip} WAS ENTER WRONG USER")
                            break
                    try:
                        if  r == True and my_dicit[client_user["user_msg"]]["pass"] ==  client_pass["user_msg"] :
                            go = libs.ready(action="TRUE_GO",user_msg=f"WELCOME {client_user["user_msg"]} TO KERNEL SERVER\nSTAY UNSEEN",user_name=client_user["user_msg"])
                            libs.send(client_socket,go)
                            if mac in failed_attemps:
                                failed_attemps[mac] = 0
                            return True
                        else:
                            libs.send(client_socket,libs.ready(user_msg="WRONG PASS",action="SENDED?"))
                            client_DONE = libs.receive_msg(client_socket)

                            if client_DONE["action"] == "YES":
                                if mac not in failed_attemps:
                                    failed_attemps[mac] = 1
                                    print(f"{client_ip} WAS ENTER WRONG PASSWORD")
                                else:
                                    failed_attemps[mac] +=  1
                                    print(f"{client_ip} WAS ENTER WRONG PASSWORD")
                                break

                            else:
                                print("error")

                    except Exception as error:
                        print(error)
                


                if failed_attemps[mac] >=3 :
                    print(f"{client_ip} IS BLOCKED")
                    black_list.append(mac)
                    return "wrong"


            # elif recv_log.lower().strip() == "logup":
            #     pass

            else:
                continue
    except Exception as error:
        print(f"ERROR : {error}")
        return False