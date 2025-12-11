import socket
import sys
import threading

class Client:

    def __init__(self):
            pass
    
    def client(host, port):
        try:
            sock = socket.socket() #créer le socket
            sock.connect((host, port)) #se connecte au serveur
            f = sock.makefile(mode="rw")

            f.write("get\n")
            f.flush()
            print(f.readline(), end="")

            f.write("quit\n")
            f.flush()
            print(f.readline(), end="")

            entree = input("Entrez une commande (get/quit) : ")
            if entree not in ["get", "quit", "Get", "Quit"]:
                print("D'autres commandes ne sont pas gérés, au revoir")
                return

            f.close()
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()

            if entree == "quit":
                print("See you some time again")
                return

    client("localhost", 5551)


   

