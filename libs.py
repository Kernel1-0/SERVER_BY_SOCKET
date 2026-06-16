# libs
HEADERSIZE = 10
def add_header(msg):
    a = f"{len(msg):<{HEADERSIZE}}" + msg
    return a
#------------------------------------
def send(sock,msg):
    sock.send(msg.encode("utf-8"))
#------------------------------------
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

    