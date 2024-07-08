import socket

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind(("192.168.196.26", 6969))
        s.listen()
        print("Attente de connexion...")
        conn, addr = s.accept()
        print(f"Connexion établie avec {addr}")

        while True:
            command = input("CMD> ")
            if command == 'exit':
                conn.send('exit'.encode("utf-8"))
                conn.close()
                break

            try:
                conn.send(command.encode("utf-8"))
                response = conn.recv(1024).decode("utf-8")
                print("Réponse du serveur:", response)
            except Exception as e:
                print("Erreur lors de la communication avec le serveur:", e)
                break

    except Exception as e:
        print("Erreur lors de l'exécution du serveur:", e)
    finally:
        s.close()

if __name__ == "__main__":
    main()
