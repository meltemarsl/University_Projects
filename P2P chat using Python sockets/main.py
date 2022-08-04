import socket
import json
import threading

MY_PORT = 12345
my_ip = 0
buffer_size = 10240
my_name = "meltem"
users = []
isListening = True


def get_my_ip():
    global my_ip
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    my_ip = s.getsockname()[0]
    print('my ip: ', my_ip)
    s.close()


class ListeningThread (threading.Thread):
    def run(self):
        while isListening:
            data = listen_w_socket()
            data_received(data)


def data_received(data):
    print('data_received: ',data )
    y = json.loads(data.decode('utf-8'))
    data_type = y["type"]
    data_name = y["name"]
    if data_type == 1:
        data_ip = y["IP"]
        DISCOVER_RESPONSE(data_name, data_ip)
    elif data_type == 2:
        print(data_name + " is here.")
    elif data_type == 3:
        data_body = y["body"]
        CHAT(data_name, data_body)


def DISCOVER_RESPONSE(data_name, data_ip):
    disc_res = {"type": 2, "name": my_name, "IP": my_ip}
    discover_r_message = json.dumps(disc_res)
    send_data_w_socket(data_ip, discover_r_message)


def CHAT(data_name, data_body):
    print("Message received from: " + data_name + " . Received message is: "+data_body)

def client(conn, addr):
    print('Connected by ',addr)
    while True:
        try:
            data = conn.recv(10240)
            print('Connected by', addr)
            print(data)
            if not data:
                break
            conn.sendall(data)
            return data
        except:
            conn.close()
            return False

def listen_w_socket():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((my_ip, MY_PORT))
        s.listen()
        while True:
            client, address = s.accept()
            client.settimeout(60)
            threading.Thread(target=client, args=(client, address)).start()


def DISCOVER():
    for i in range(55,62):
        ip = "192.168.43." + str(i)
        disc_message = {"type": 1, "name": my_name, "IP": my_ip}
        discover_message = json.dumps(disc_message)
        msg_from_discovered = send_data_w_socket(ip, discover_message)
        if msg_from_discovered:
            print(ip, ' is online.')
            users.append(ip)
        else:
            print("continue: ", ip)
            continue


def send_data_w_socket(ip, data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        socket.setdefaulttimeout(0.1)
        try:
            s.connect((ip, MY_PORT))
            print("connected to: ", ip)
            s.sendall(data.encode('utf-8'))
            data_r = s.recv(1024)
            print('Received', repr(data_r))
            return data_r
        except:
            print("returning false")
            return False


if __name__ == '__main__':
    get_my_ip()
    #send_data_w_socket("discover me")
    print("here")
    thread1 = ListeningThread()
    thread1.start()
    DISCOVER()
    #listen_w_socket()
    while(True):
        print("Enter an IP or type 'list' to see active users")
        message = input()
        m = {"type": 3, "name": my_name, "body": message}
        smessage = json.dumps(m)
        if message == "list":
            for i in users:
                print(i)
        print("Enter an IP")
        IPP = input()
        print("Enter your message: ")
        smessage = input()
        send_data_w_socket(IPP, smessage)

