"""
Classe chiffrement Diffie-Hellman
Source : https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange#Cryptographic_explanation
"""
import random
import math
from math import gcd as bltin_gcd


class DiffieHellman:
    """Classe de chiffrement Diffie-Hellman"""

    def generer_public_params(self, taille_bits=2048):
        """Génère les paramètres publics p et g."""
        p = self.generer_prime(taille_bits)
        g = self.generer_generator(p)
        return p, g

    def generer_prime(self, taille_bits):
        """Génère un nombre premier aléatoire de la taille spécifiée en bits."""
        while True:
            nombre = random.getrandbits(taille_bits)
            if self.est_premier(nombre):
                return nombre

    def generer_generator(self, p):
        """Génère un générateur pour le nombre premier p. (primitive root modulo p)"""
        # https://stackoverflow.com/questions/40190849/efficient-finding-primitive-roots-modulo-n-using-python
        required_set = {num for num in range(1, p) if bltin_gcd(num, p)}
        return min([
            g for g in range(1, p)
            if required_set == {pow(g, powers, p)
                                for powers in range(1, p)}
        ])

    def est_premier(self, x):
        """Retourne True si x est un nombre premier, False sinon."""
        return x != 1 and all(x % i != 0
                              for i in range(2,
                                             int(math.sqrt(x)) + 1))

    def choisir_secret(self, p):
        """Choisit un entier secret aléatoire dans l'intervalle [2, p-2]."""
        return random.randint(2, p - 2)

    def calculer_clef_partagee(self, clef_publique_autre, secret, p):
        """Calcule la clef partagée en utilisant la clef publique de l'autre partie, son propre secret
        et le nombre premier p."""
        return pow(clef_publique_autre, secret, p)

    def calculer_clef_publique(self, g, secret, p):
        """Calcule la clef publique en utilisant le générateur g, son propre secret et le nombre premier p."""
        return pow(g, secret, p)
