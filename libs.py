# libs
HEADERSIZE = 10
def add_header(msg):
    a = f"{len(msg):<{HEADERSIZE}}" + msg
    return a
#------------------------------------
def send(sock,msg):
    import json
    json_string = json.dumps(msg)
    msg_with_header = add_header(json_string)

    sock.send(msg_with_header.encode("utf-8"))
#------------------------------------
def receive_msg(sock):
    import json
    full_msg = ""
    new_msg = True
    msg_len = 0

    while True:
        msg = sock.recv(2048)
        msg_decoded = msg.decode("utf-8")

        if not msg:
            break
            # for attemp in range(1,11):
            #     msg = sock.recv(2048)
            #     msg_decoded = msg.decode("utf-8")
            #     if msg:
            #         break
            #     if not msg and attemp >= 10:
            #         return False
            

        if new_msg:
            msg_len = int(msg_decoded[:HEADERSIZE])    
            new_msg = False

        full_msg += msg_decoded


        if len(full_msg) - HEADERSIZE == msg_len:
            actual_msg = full_msg[HEADERSIZE:]
            return json.loads(actual_msg)
        
#------------------------------------

def get_client_mac(client_ip):
    try:
        import subprocess
        arp_output = subprocess.check_output(f"arp -an {client_ip}",shell=True).decode()
        for word in arp_output.split():
            if ":" in word and len(word) == 17:
                return word
    except Exception:
        return False

def ready(action="new_alert",user_msg="close",role="NONE",user_name="ANONYMOUS",hint="hint"):
        return {
        "action" : action,
        "user_msg" : user_msg,
        "role" : role,
        "user_name" : user_name,
        "hint" : hint
        }
