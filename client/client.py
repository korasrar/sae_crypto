import socket
from threading import Thread, Lock
import time


class Client:
    """classe Client"""

    def __init__(self, host="localhost", port=15001):
        """Initialise le client
        Args:
            host (str): Adresse du serveur
            port (int): Port du serveur
        """
        self.host = host
        self.port = port
        self.socket = None
        self.fichier = None
        self.couleur = None  
        self.en_partie = False
        self.partie_trouvee = False
        self.verrou = Lock()
        self.connecte = False
        self.nom_joueur = None
        self.dernier_coup_adversaire = None

    def connecter(self):
        """se connecte au serveur"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.fichier = self.socket.makefile(mode="rw")
            self.connecte = True
            print(f"connecté au serveur tel que {self.host}:{self.port}")

            thread_ecoute = Thread(target=self.ecouter_serveur, daemon=True)
            thread_ecoute.start()

            return True
        except Exception as e:
            print(f"il ya une erreure inatendue : {e}")
            return False

    def envoyer(self, message):
        """envoie un message au serveur"""
        try:
            with self.verrou:
                self.fichier.write(message + "\n")
                self.fichier.flush()
        except Exception as e:
            print(f"le client n'a pas pu envoyer le message: {e}")
            self.connecte = False

    def recevoir(self):
        """reçoit un message du serveur"""
        try:
            ligne = self.fichier.readline().strip()
            return ligne
        except:
            self.connecte = False
            return None

    def ecouter_serveur(self):
        """écoute les messages du serveur"""
        while self.connecte:
            try:
                message = self.recevoir()
                if not message:
                    break
                self.traiter_message(message)
            except:
                break

        self.connecte = False

    def traiter_message(self, message):
        """traite les messages reçus du serveur"""
        parties = message.split() 
        if not parties:
            return
        commande = parties[0]
        if commande == "OK":
            pass  
        elif commande == "ERR":
            erreur = " ".join(parties[1:])
            print(f"il ya une erreur recue du serveur : {erreur}")

        elif commande == "start":

            if len(parties) > 1:
                self.couleur = parties[1]
                self.en_partie = True
                self.partie_trouvee = True
                print(f"La partie a commencée! vous jouez les {'Blancs' if self.couleur == 'w' else 'Noirs'}")

        elif commande == "play":

            if len(parties) >= 3:
                case_src = parties[1]
                case_dst = parties[2]
                self.dernier_coup_adversaire = (case_src, case_dst)

        elif commande == "win":
            print("Vous avez gagné! l'adversaire a abandonné... bouuuu")
            self.en_partie = False

        elif commande == "lose":
            print("Vous avez perdu par abandon.")
            self.en_partie = False

    def register(self, nom_joueur, mot_de_passe):
        """enregistre un nouveau joueur"""
        self.envoyer(f"register {nom_joueur} {mot_de_passe}")
        time.sleep(2)  

    def login(self, nom_joueur, mot_de_passe):
        """se connecte avec un compte"""
        self.nom_joueur = nom_joueur
        self.envoyer(f"connect {nom_joueur} {mot_de_passe}")
        time.sleep(2)

    def chercher_partie(self):
        """cherche une partie"""
        self.envoyer("new")

    def jouer_coup(self, case_src, case_dst):
        """envoie un coup au serveur"""
        self.envoyer(f"play {case_src} {case_dst}")

    def abandonner(self):
        """abandonne la partie"""
        self.envoyer("leave")

    def quitter(self):
        """quitte et ferme la connexion"""
        self.envoyer("quit")
        self.connecte = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass