import datetime
import socket
import json
import threading

PORT = 12345
my_ip = 0
buffer_size = 10240
my_name = ""
users = {}
IDs = []
isListening = True

def get_my_ip():
    global my_ip
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    my_ip = s.getsockname()[0]
    s.close()

class ListeningThreadUDP (threading.Thread):
    def run(self):
        while isListening:
            data = listen_UDP()
            data_received(data)
def listen_UDP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((my_ip, PORT))
    while True:
        msg, addr = s.recvfrom(buffer_size)
        return (msg)

class ListeningThreadTCP (threading.Thread):
    def run(self):
        while isListening:
            data= listen_TCP()
            data_received(data)
def listen_TCP():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((my_ip, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                #print("Connected by", addr)
                while True:
                    data = conn.recv(buffer_size)
                    if not data:
                        break
                    conn.sendall(data)
                    return data

def data_received(data):
    y = json.loads(data.decode('utf-8'))
    data_type = y["type"]
    data_name = y["name"]
    #print('Received data: ', data, 'from ', data_name)
    if data_type == 1:
        data_ip = y["IP"]
        data_ID = y["ID"]
        if data_ID not in IDs:
            IDs.append(data_ID)
            DISCOVER_RESPONSE(data_name, data_ip)
    elif data_type == 2:
        data_ip = y["IP"]
        print(data_name + " is here.")
        users[data_name] = data_ip
    elif data_type == 3:
        data_body = y["body"]
        CHAT(data_name, data_body)

def DISCOVER():
    for j in range(10):
        disc_message = {"ID": int(datetime.datetime.now().timestamp()), "type": 1, "name": my_name, "IP": my_ip}
        discover_message = json.dumps(disc_message)
        send_data_w_UDP(discover_message)
def DISCOVER_RESPONSE(data_name, data_ip):
    users[data_name] = data_ip
    print(data_name,'is here.')
    disc_res = {"type": 2, "name": my_name, "IP": my_ip}
    discover_r_message = json.dumps(disc_res)
    send_data_w_TCP(data_name, discover_r_message)

def CHAT(data_name, data_body):
    print("Message received from: " + data_name + " . Received message is: "+data_body)

def send_data_w_UDP(data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((my_ip, 0))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(data.encode('utf-8'), ('<broadcast>', PORT))
    sock.close()

def send_data_w_TCP(name, data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((users[name], PORT))
        except:
            users[name] = 0
        #("connected to: ", ip)
        s.sendall(data.encode('utf-8'))
        data_r = s.recv(1024)
        return data_r

if __name__ == '__main__':
    get_my_ip()
    print("What is your name? ")
    my_name = input()
    if my_name == "":
        print("Please enter a name!!!")
        my_name = input()
    if my_name == "":
        print("You know")
        exit()
    thread_UDP = ListeningThreadUDP()
    thread_UDP.start()
    thread_TCP = ListeningThreadTCP()
    thread_TCP.start()
    DISCOVER()
    while(True):
        print("Enter an name or type 'list' to see active users")
        message = input()
        if message == "list":
            print("Active Users: ")
            for name, _id in users.items():
                if users[name] != 0:
                    print(name)
            continue
        try:
            print("Your message: ")
            message = input()
            m = {"ID": int(datetime.datetime.now().timestamp()), "type": 3, "name": my_name, "body": message}
            smessage = json.dumps(m)
            send_data_w_TCP(name, smessage)
        except:
            print("User not found")
