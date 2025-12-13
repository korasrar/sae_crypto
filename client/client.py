import socket
from threading import Thread, Lock
import time
import chess


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
        self.board = chess.Board()

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
                self.board.reset()
                couleur_nom = "Blancs" if self.couleur == 'w' else "Noirs"
                print(f"\nLa partie commence! vous jouez les {couleur_nom}")
                self.affiche_plateau()

        elif commande == "play":
            if len(parties) >= 3:
                case_src = parties[1]
                case_dst = parties[2]
                self.appliquer_coup_adversaire(case_src, case_dst)

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

    def appliquer_coup_adversaire(self, case_src, case_dst):
        """applique le coup de l'adversaire sur le plateau"""
        try:
            move1 = case_src + case_dst
            move = chess.Move.from_uci(move1)

            if move in self.board.legal_moves:
                self.board.push(move)
                print(f"\n l'adversaire a joué: {case_src} → {case_dst}")
                self.affiche_plateau()

                if self.board.is_game_over():
                    self.afficher_fin_partie()
            else:
                print(
                    f"attention, il y a un coup illégal de l'adversaire: {move1}"
                )
        except Exception as e:
            print(f"erreur lors de l'application du coup: {e}")

    def affiche_plateau(self):
        """affiche le plateau d'échecs"""
        print("\n" + "=" * 40)
        print(self.board.unicode())
        print("=" * 40)

        if self.en_partie:
            tour = "Blancs" if self.board.turn == chess.WHITE else "Noirs"
            print(f"C'est aux tours des {tour}")

            if self.couleur:
                ma_couleur = "Blancs" if self.couleur == 'w' else "Noirs"
                print(f"Vous êtes: {ma_couleur}")

    def est_mon_tour(self):
        """vérifie si c'est le tour du joueur"""
        if not self.en_partie or not self.couleur:
            return False

        if self.couleur == 'w':
            return self.board.turn == chess.WHITE
        else:
            return self.board.turn == chess.BLACK

    def afficher_fin_partie(self):
        """affiche le résultat de la partie"""
        outcome = self.board.outcome()
        if outcome:
            print("\n" + "=" * 40)
            print("FIN DE LA PARTIE")

            if outcome.winner == chess.WHITE:
                print("Les Blancs ont gagné!")
            elif outcome.winner == chess.BLACK:
                print("Les Noirs ont gagné!")
            else:
                print("Match nul car exæquo!")

            print(f"message: {outcome.termination.name}")
            print("=" * 40)
            self.en_partie = False

    def afficher_coups_legaux(self):
        """affiche tous les coups légaux possibles"""
        if not self.en_partie:
            print("il n'y a pas de partie en cours!")
            return

        legal_moves = list(self.board.legal_moves)
        if not legal_moves:
            print("il n'y a aucun coup correct disponible...")
