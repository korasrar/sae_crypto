import Piece
import numpy as np

class Plateau:

    def __init__(self, taille=8):
        self._taille = taille
        self._pieces = self.initialiser_plateau()

    def initialiser_plateau(self):
        lignes = []
        for _ in range(self._taille):
            colonnes = []
            for _ in range(self._taille):
                colonnes.append(None)
            lignes.append(colonnes)
        return lignes
                
    def obtenir_piece(self):
        return self._pieces

    def placer_pieces(self):
        pass

    def deplacer_pieces(self):
        pass

    def afficher (self):
        print(np.matrix(self._pieces))

    def est_en_echec(self, couleur):
        pass

    def  get_taille(self):
        return self._taille
    
    def set_taille(self, taille):
        self._taille = taille
        self._pieces = self.initialiser_plateau()

    def get_pieces(self):
        return self._pieces
    
    def set_pieces(self, pieces):
        self._pieces = pieces

