"""
Module Server et Session pour la sae_crypto
"""
import socket
from threading import Thread, Lock

joueurs_enregistres = {}
joueurs_connectes = {}
joueurs_en_attente = []
parties_actives = {}
verrou_joueurs = Lock()


class Serveur:
    """
    Classe Serveur qui s'occupe de la réception des connexions joueurs
    """
    def __init__(self):
        self.compteur = 0

    def demarrer(self, port):
        """permet de démarrer le serveur sur le port donné et d'attendre les connexions

        Args:
            port (int): port d'écoute du serveur
        """
        socket_serveur = socket.socket()
        socket_serveur.bind(("0.0.0.0", port))
        socket_serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_serveur.listen(2)
        print(f"Serveur démarré sur le port {port}")
        while True:
            client, adresse = socket_serveur.accept()
            print(f"Nouvelle connexion de {adresse}")
            session = Session(self, client)


class Session(Thread):
    """Classe Session qui s'occupe de la communication avec un client

    Args:
        Thread (): hérite de Thread
    """

    # dico des commandes
    COMMANDES = {
        "register": "cmd_register",
        "connect": "cmd_connect",
        "play": "cmd_play",
        "leave": "cmd_leave",
        "quit": "cmd_quit",
        "replay": "cmd_replay",
        "new": "cmd_new"
    }

    def __init__(self, serveur, sock):
        Thread.__init__(self)
        self.serveur = serveur
        self.socket = sock
        self.fichier = sock.makefile(mode="rw")
        self.verrou = Lock()
        self.nom_joueur = None
        self.en_partie = False
        self.adversaire = None
        self.couleur = None  # 'w' ou 'b'
        self.attend_replay = False
        self.start()

    def envoyer(self, message):
        """Envoie un message au client"""
        with self.verrou:
            self.fichier.write(message + "\n")
            self.fichier.flush()

    def envoyer_ok(self):
        """Envoie une réponse OK"""
        self.envoyer("OK")

    def envoyer_erreur(self, message):
        """Envoie une réponse d'erreur"""
        self.envoyer(f"ERR {message}")

    def cmd_register(self, args):
        """
        register nomJoueur motDePasse : enregistre un nouveau joueur
        - nomJoueur: 3-10 caractères, sans espace
        - motDePasse: au moins 6 caractères
        """
        if len(args) < 2:
            self.envoyer_erreur("Usage: register nomJoueur motDePasse")
            return

        nom_joueur = args[0]
        mot_de_passe = args[1]

        if len(nom_joueur) < 3 or len(nom_joueur) > 10:
            self.envoyer_erreur(
                "Le nom du joueur doit avoir entre 3 et 10 caracteres")
            return

        if " " in nom_joueur:
            self.envoyer_erreur(
                "Le nom du joueur ne doit pas contenir d'espace")
            return

        if len(mot_de_passe) < 6:
            self.envoyer_erreur(
                "Le mot de passe doit avoir au moins 6 caracteres")
            return

        with verrou_joueurs:
            if nom_joueur in joueurs_enregistres:
                self.envoyer_erreur("Ce joueur existe deja")
                return

            joueurs_enregistres[nom_joueur] = mot_de_passe

        self.envoyer_ok()

    def cmd_connect(self, args):
        """
        connect nomJoueur motDePasse : demande de connexion du client
        """
        if len(args) < 2:
            self.envoyer_erreur("Usage: connect nomJoueur motDePasse")
            return

        nom_joueur = args[0]
        mot_de_passe = args[1]

        if nom_joueur in joueurs_connectes:
            self.envoyer_erreur("Le joueur est déjà présent dans la partie")
            return

        if nom_joueur not in joueurs_enregistres:
            self.envoyer_erreur("Le nom du joueur n'est pas register")
            return

        if joueurs_enregistres[nom_joueur] != mot_de_passe:
            self.envoyer_erreur("Le mot de passe n'est pas correct")
            return

        joueurs_connectes[nom_joueur] = mot_de_passe

        self.envoyer_ok()

        with verrou_joueurs:
            if self.adversaire:
                self.adversaire.envoyer(f"start {self.adversaire.couleur}")
                self.envoyer(f"start {self.couleur}")
            else:
                joueurs_en_attente.append(self)

    def cmd_play(self, args):
        """
        play caseSrc caseDst : déplace une pièce
        Format: a3 a4
        """
        if not self.en_partie:
            self.envoyer_erreur("Vous n'êtes pas dans une partie")
            return
        
        case_source = args[0]
        case_destination = args[1]

        # Coups deja vérifier par le client
        self.envoyer_ok()

        if self.adversaire:
            self.adversaire.envoyer(f"play {case_source} {case_destination}")

    def cmd_leave(self, args):
        """
        leave : le client abandonne la partie
        """
        if not self.en_partie:
            self.envoyer_erreur("Aucune partie en cours")
            return

        with verrou_joueurs:
            if self.adversaire:
                self.adversaire.envoyer("win")
                self.adversaire.en_partie = False
                self.adversaire.adversaire = None

                if self in parties_actives:
                    del parties_actives[self]
                if self.adversaire in parties_actives:
                    del parties_actives[self.adversaire]

            self.en_partie = False
            self.adversaire = None

        self.envoyer_ok()
        self.envoyer("lose")

    def cmd_quit(self, args):
        """
        quit : le client quitte et ferme la connexion
        """
        with verrou_joueurs:
            # partie en cours
            if self.en_partie and self.adversaire:
                self.adversaire.envoyer("win")
                self.adversaire.en_partie = False
                self.adversaire.adversaire = None

                if self in parties_actives:
                    del parties_actives[self]
                if self.adversaire in parties_actives:
                    del parties_actives[self.adversaire]

            if self in joueurs_en_attente:
                joueurs_en_attente.remove(self)

            if self.nom_joueur and self.nom_joueur in joueurs_connectes:
                del joueurs_connectes[self.nom_joueur]

        self.envoyer_ok()
        return True

    def cmd_replay(self, args):
        """
        replay : relance le jeu contre le même adversaire
        Les deux joueurs doivent avoir envoyé cette commande
        """
        if not self.en_partie or not self.adversaire:
            self.envoyer_erreur("Aucune partie en cours")
            return

        if self.attend_replay:
            self.envoyer_erreur("Vous avez déjà demandé un replay")
            return

        self.attend_replay = True
        self.envoyer_ok()

        if self.adversaire.attend_replay:
            self.attend_replay = False
            self.adversaire.attend_replay = False

            self.couleur, self.adversaire.couleur = (self.adversaire.couleur,
                                                     self.couleur)

            self.envoyer(f"start {self.couleur}")
            self.adversaire.envoyer(f"start {self.adversaire.couleur}")

    def cmd_new(self, args):
        """
        new : à la fin d'une partie, cherche un nouvel adversaire
        """
        if self.en_partie:
            self.envoyer_erreur("Une partie est deja en cours")
            return

        with verrou_joueurs:
            self.adversaire = None
            self.attend_replay = False

            if joueurs_en_attente:
                session_adversaire = joueurs_en_attente.pop(0)
                self.adversaire = session_adversaire
                session_adversaire.adversaire = self

                self.couleur = 'b'
                session_adversaire.couleur = 'w'

                self.en_partie = True
                session_adversaire.en_partie = True

                parties_actives[self] = session_adversaire
                parties_actives[session_adversaire] = self

        self.envoyer_ok()

        with verrou_joueurs:
            if self.adversaire:
                self.adversaire.envoyer(f"start {self.adversaire.couleur}")
                self.envoyer(f"start {self.couleur}")
            else:
                joueurs_en_attente.append(self)

    def construire_commande(self, ligne):
        """
        Builder: parse la ligne reçue et appelle la fonction correspondante
        Retourne True si la connexion doit être fermée
        """
        if not ligne:
            return False

        parties = ligne.split()
        if not parties:
            self.envoyer_erreur("Commande vide")
            return False

        commande = parties[0].lower()
        arguments = parties[1:]

        if commande in self.COMMANDES:
            nom_methode = self.COMMANDES[commande]
            methode = getattr(self, nom_methode)
            resultat = methode(arguments)
            return resultat is True
        else:
            self.envoyer_erreur(f"Commande inconnue: {commande}")
            return False

    def run(self):
        try:
            while True:
                # méthode bloquante, on attend de recevoir une string
                ligne = self.fichier.readline().strip()

                if not ligne:
                    break

                doit_fermer = self.construire_commande(ligne)

                if doit_fermer:
                    break

        except Exception as e:
            print(f"Erreur session: {e}")
        finally:
            self.nettoyer()

    def nettoyer(self):
        """Nettoie la session lors de la déconnexion"""
        with verrou_joueurs:
            if self.en_partie and self.adversaire:
                self.adversaire.envoyer("win")
                self.adversaire.en_partie = False
                self.adversaire.adversaire = None

            if self in joueurs_en_attente:
                joueurs_en_attente.remove(self)

            if self.nom_joueur and self.nom_joueur in joueurs_connectes:
                del joueurs_connectes[self.nom_joueur]

            if self in parties_actives:
                del parties_actives[self]

        try:
            self.fichier.close()
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
        except:
            pass


if __name__ == "__main__":
    Serveur().demarrer(15001)
