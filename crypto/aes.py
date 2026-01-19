from cryptography.fernet import Fernet
from crypto import diffie_hellman
from serveur import serveur
from client import client


class ChiffrementAES:
    
    def __init__(self, cle=None):
        if cle is None:
            self.cle = Fernet.generate_key()
        else:
            self.cle = cle
        self.fernet = Fernet(self.cle)
    
    def obtenir_cle(self):
        return self.cle
    
    def set_cle(self, new_cle):
        self.cle = new_cle
            
    def chiffrer(self, message):
        return self.fernet.encrypt(message.encode()).decode()
    
    def dechiffrer(self, message_chiffre):
        return self.fernet.decrypt(message_chiffre.encode()).decode()
