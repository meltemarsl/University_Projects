import json
import threading
import socket
import subprocess

MY_PORT = "12345"
my_ip = ""
my_name = "meltem"
users = {}
isListening = True

class ListeningThread (threading.Thread):
    def run(self):
        while(isListening):
            data, self.process = listen()
            data_received(data)
    def kill(self):
        self.process.kill()



def data_received(data):
    y = json.loads(data)
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


def DISCOVER():
    for i in range(1,255):
        ip = "192.168.1." + str(i)
        discover_message = '''{ "type":1, "name":"'''+ my_name +'''", "IP":"'''+my_ip +'''"}'''
        send_data(ip, discover_message)

def DISCOVER_RESPONSE(data_name, data_ip):
    users[data_name] = data_ip
    discover_r_message = '''{ "type":2, "name":"''' + my_name + '''", "IP":"''' + my_ip + '''"}'''
    send_data(data_ip, discover_r_message)


def CHAT(data_name, data_body):
    print("Message received from: "+ data_name+ " . Received message is: "+data_body)


def get_my_ip():
    global my_ip
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    my_ip = s.getsockname()[0]
    s.close()

def listen():
    listen_process = subprocess.run(["ncat", "-lp", MY_PORT], text=True, stdout=subprocess.PIPE)
    return listen_process.stdout, listen_process

def send_data(ip, data):
    echo = subprocess.Popen(["echo", data], stdout=subprocess.PIPE)
    subprocess.Popen(["ncat", ip, MY_PORT], stdin=echo.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


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
    DISCOVER()
    thread1 = ListeningThread()
    thread1.start()
    while(True):
        print("Type 'active-users' to see active users,OR enter a username")
        name = input()
        if(name == "active-users"):
            print("Active Users")
            for name, _id in users.items():
                print(name)
            continue
        if(name == "0"):
            print("Goodbye!")
            exit()
        try:
            ipp = users[name]
            print("Your message: ")
            message = input()
            smessage = '''{ "type":3, "name":"''' + my_name + '''", "body":"''' + message + '''"}'''
            send_data(users[name], smessage)
        except:
            print("User not found")
    exit()
