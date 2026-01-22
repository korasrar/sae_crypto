from cryptography.fernet import Fernet
import base64
import hashlib


class ChiffrementAES:

    def __init__(self, cle=None):
        if cle is None:
            self.cle = Fernet.generate_key()
        else:
            self.cle = cle
        self.fernet = Fernet(self.cle)

    def obtenir_cle(self):
        return self.cle

    def set_clef(self, new_clef):
        cle_bytes = str(new_clef).encode()

        cle_hachee = hashlib.sha256(cle_bytes).digest()

        # "Fernet key must be 32 url-safe base64-encoded bytes."
        # ca viens du code de la librairie cryptography
        self.cle = base64.urlsafe_b64encode(cle_hachee)
        self.fernet = Fernet(self.cle)

    def chiffrer(self, message):
        return self.fernet.encrypt(message.encode()).decode()

    def dechiffrer(self, message_chiffre):
        try:
            message_dechiffre = self.fernet.decrypt(
                message_chiffre.encode()).decode()
        except Exception:
            return None
        return message_dechiffre
