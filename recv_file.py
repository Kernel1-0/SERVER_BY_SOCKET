# auth
import libs

login_password = "123"

black_list = []
failed_attemps = {}

def login(client_socket,client_ip):
    mac = libs.get_client_mac(client_ip)
    if mac in black_list:
        print(f"The {client_ip} was fucked👍")
        fail_msg =  libs.add_header("FUCK YOU\nYOUR MAC IS BLACKLISTED!")
        libs.send(client_socket,fail_msg)
        return False
    

    msg = libs.add_header("PASSWORD_REQUIRED")
    libs.send(client_socket,msg)

    client_input = client_socket.recv(1024).decode("utf-8").strip()


    if client_input == login_password:
        libs.send(client_socket,libs.add_header("WELCOME TO KERNEL SERVER\nSTAY UNSEEN"))
        if mac in failed_attemps:
            failed_attemps[mac] = 0
        return True
    else:
        libs.send(client_socket,libs.add_header("FUCK YOU\nGET OUT NOWW!"))
        if mac not in failed_attemps:
            failed_attemps[mac] = 1
            print(f"{client_ip} WAS ENTER WRONG PASSWORD")


        else:
            failed_attemps[mac] +=  1
            print(f"{client_ip} WAS ENTER WRONG PASSWORD")
        
        if failed_attemps[mac] >=3 :

            print(f"{client_socket} IS BLOCKED")
            black_list.append(mac)


        return "wrong"

