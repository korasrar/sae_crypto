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
        self.derniere_reponse = None
        self.attente_reponse = False

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
            print(f"il ya une erreur inatendue : {e}")
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
            self.derniere_reponse = "OK"
            self.attente_reponse = False
        elif commande == "ERR":
            erreur = " ".join(parties[1:])
            self.derniere_reponse = f"ERR {erreur}"
            self.attente_reponse = False
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

    def attendre_reponse(self, timeout=5):
        """attend une réponse du serveur avec un timeout"""
        self.attente_reponse = True
        self.derniere_reponse = None
        debut = time.time()
        while self.attente_reponse and (time.time() - debut) < timeout:
            time.sleep(0.1)
        return self.derniere_reponse

    def register(self, nom_joueur, mot_de_passe):
        """enregistre un nouveau joueur"""
        self.envoyer(f"register {nom_joueur} {mot_de_passe}")
        reponse = self.attendre_reponse()
        if reponse == "OK":
            print("Enregistrement réussi.")
            return True
        elif reponse and reponse.startswith("ERR"):
            return False
        else:
            print("Timeout: pas de réponse du serveur.")
            return False

    def login(self, nom_joueur, mot_de_passe):
        """se connecte avec un compte"""
        self.envoyer(f"connect {nom_joueur} {mot_de_passe}")
        reponse = self.attendre_reponse()
        if reponse == "OK":
            self.nom_joueur = nom_joueur
            print("Connexion réussie.")
            return True
        elif reponse and reponse.startswith("ERR"):
            return False
        else:
            print("Timeout: pas de réponse du serveur.")
            return False

    def chercher_partie(self):
        """cherche une partie"""
        self.envoyer("new")
        reponse = self.attendre_reponse()
        if reponse == "OK":
            print("Recherche de partie lancée...")
            return True
        elif reponse and reponse.startswith("ERR"):
            return False
        else:
            print("Timeout: pas de réponse du serveur.")
            return False

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

        print("\nCoups légaux disponibles:")
        moves_str = [move.uci() for move in legal_moves]
        print(" | ".join(moves_str))

    def abandonner_partie(self):
        """abandonne la partie en cours"""
        if self.en_partie:
            self.envoyer("leave")
            reponse = self.attendre_reponse()
            if reponse == "OK":
                self.en_partie = False
                print("Vous avez abandonné la partie.")
                return True
            elif reponse and reponse.startswith("ERR"):
                return False
            else:
                print("Timeout: pas de réponse du serveur.")
                return False
        else:
            print("il n'y a pas de partie en cours à abandonner.")
            return False

    def menu_principal(self):
        """affiche le menu principal"""
        print("1: Partie Locale")
        print("2: Partie en ligne")
        print("3: Historique des parties")
        print("4: quitter")

    def lancer_client(self):
        """lance le menu principal du client"""
        quitter = False
        while not quitter:
            self.menu_principal()
            choix = input("Choisissez une option \n")

            match choix:
                case "1":
                    print("Fonctionnalité à implementer")
                case "2":
                    self.lancer_menu_connection()
                case "3":
                    print("Fonctionnalité à implementer")
                case "4":
                    quitter = True
        print("fermeture du client...")

    def menu_connection(self):
        """affiche le menu de connexion"""
        print("1: S'enregistrer")
        print("2: Se connecter")
        print("3: Quitter")

    def lancer_menu_connection(self):
        """lance le menu de connexion"""
        quitter = False
        while not quitter:
            self.menu_connection()
            choix = input("Choisissez une option \n")

            match choix:
                case "1":
                    nom = input("Entrez le nom d'utilisateur: ")
                    mot_de_passe = input("Entrez le mot de passe: ")
                    if self.register(nom, mot_de_passe):
                        print("Vous pouvez maintenant vous connecter.")
                case "2":
                    nom = input("Entrez le nom d'utilisateur: ")
                    mot_de_passe = input("Entrez le mot de passe: ")
                    if self.login(nom, mot_de_passe):
                        self.lancer_menu_partie_en_ligne()
                case "3":
                    quitter = True
        print("fermeture du client...")

    def menu_partie_en_ligne(self):
        """affiche le menu de la partie en ligne"""
        print("1: Chercher une partie")
        print("2: Abandonner la partie")
        print("3: Quitter au menu principal")

    def lancer_menu_partie_en_ligne(self):
        """lance le menu de la partie en ligne"""
        quitter = False
        while not quitter:
            self.menu_partie_en_ligne()
            choix = input("Choisissez une option \n")

            match choix:
                case "1":
                    if self.chercher_partie():
                        self.lancer_menu_en_jeu()
                case "2":
                    self.abandonner_partie()
                case "3":
                    quitter = True
        print("Retour au menu principal...")

    def menu_en_jeu(self):
        """affiche le menu des commandes disponibles en partie"""
        print("\n" + "=" * 40)
        print("COMMANDES DISPONIBLES:")
        print("  [move] <src> <dst> : Jouer un coup (ex: move e2 e4)")
        print("  [legal]            : Afficher les coups légaux")
        print("  [board]            : Afficher le plateau")
        print("  [resign]           : Abandonner la partie")
        print("  [replay]           : Demander une revanche")
        print("  [quit]             : Quitter la partie")
        print("=" * 40)

    def lancer_menu_en_jeu(self):
        """lance le menu de jeu quand une partie est en cours"""
        print("\nEn attente d'un adversaire...")

        while not self.partie_trouvee and self.connecte:
            time.sleep(0.5)

        if not self.partie_trouvee:
            print("La connexion a été perdue.")
            return

        while self.en_partie and self.connecte:
            if self.est_mon_tour():
                self.menu_en_jeu()
                commande = input("\nC'est votre tour! Entrez une commande: "
                                 ).strip().lower()
                self.traiter_commande_jeu(commande)
            else:
                print("\nC'est au tour de l'adversaire, veuillez patienter...")
                while not self.est_mon_tour(
                ) and self.en_partie and self.connecte:
                    time.sleep(0.3)

        print("\nLa partie est terminée.")
        self.partie_trouvee = False

    def traiter_commande_jeu(self, commande):
        """traite les commandes entrées pendant le jeu"""
        parties = commande.split()
        if not parties:
            return

        cmd = parties[0]

        if cmd == "move":
            if len(parties) >= 3:
                case_src = parties[1]
                case_dst = parties[2]
                self.jouer_coup(case_src, case_dst)
            elif len(parties) == 2 and len(parties[1]) == 4:
                move_str = parties[1]
                case_src = move_str[:2]
                case_dst = move_str[2:]
                self.jouer_coup(case_src, case_dst)
            else:
                print("Usage: move <src> <dst> (ex: move e2 e4)")

        elif cmd == "legal":
            self.afficher_coups_legaux()

        elif cmd == "board":
            self.affiche_plateau()

        elif cmd == "resign":
            self.abandonner_partie()

        elif cmd == "replay":
            self.demander_replay()

        elif cmd == "quit":
            self.quitter_partie()

        elif cmd == "help":
            self.menu_en_jeu()

        else:
            print(
                f"Commande inconnue: {cmd}. Tapez 'help' pour voir les commandes."
            )

    def jouer_coup(self, case_src, case_dst):
        """joue un coup et l'envoie au serveur"""
        try:
            move_uci = case_src + case_dst
            move = chess.Move.from_uci(move_uci)

            if move not in self.board.legal_moves:
                print(f"Coup illégal: {case_src} → {case_dst}")
                return False

            self.envoyer(f"play {case_src} {case_dst}")
            reponse = self.attendre_reponse()

            if reponse == "OK":
                self.board.push(move)
                print(f"Vous avez joué: {case_src} → {case_dst}")
                self.affiche_plateau()

                if self.board.is_game_over():
                    self.afficher_fin_partie()

                return True
            elif reponse and reponse.startswith("ERR"):
                return False
            else:
                print("Timeout: pas de réponse du serveur.")
                return False
        except Exception as e:
            print(f"Erreur lors du coup: {e}")
            return False

    def demander_replay(self):
        """demande une revanche"""
        if self.en_partie:
            self.envoyer("replay")
            reponse = self.attendre_reponse()
            if reponse == "OK":
                print(
                    "Demande de revanche envoyée. En attente de l'adversaire..."
                )
                return True
            elif reponse and reponse.startswith("ERR"):
                return False
            else:
                print("Timeout: pas de réponse du serveur.")
                return False
        else:
            print("Pas de partie en cours.")
            return False

    def quitter_partie(self):
        """quitte la partie en cours"""
        if self.en_partie:
            self.envoyer("leave")
            reponse = self.attendre_reponse()
            if reponse == "OK":
                self.en_partie = False
                print("Vous avez quitté la partie.")
                return True
            elif reponse and reponse.startswith("ERR"):
                return False
            else:
                print("Timeout: pas de réponse du serveur.")
                return False
        else:
            print("Pas de partie en cours.")
            return False


if __name__ == "__main__":
    client = Client()
    if client.connecter():
        client.lancer_client()
