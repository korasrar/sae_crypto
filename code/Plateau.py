import Piece

class Plateau:

    def __init__(self, taille=8):
        self._taille = taille
        self._pieces = [[None for _ in range(self._taille)] for _ in range(self._taille)]

    def initialiser_plateau(self):
        pass

    def obtenir_piece(self):
        pass

    def placer_pieces(self):
        pass

    def deplacer_pieces(self):
        pass

    def afficher (self):
        pass

    def est_en_echec(self, couleur):
        pass

    def  get_taille(self):
        return self._taille
    
    def set_taille(self, taille):
        self._taille = taille

    def get_pieces(self):
        return self._pieces
    
    def set_pieces(self, pieces):
        self._pieces = pieces

