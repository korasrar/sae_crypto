class Piece:

    def __init__(self, couleur, position):
        """Initialise une pièce avec une couleur et une position
        Args:
            couleur (str): une couleur de pièce
            position (liste): liste de tuple represetant une position (x,y) sur le plateau
        """

        self._couleur = couleur
        self._position = position

    def get_couleur(self):
        return self._couleur
    
    def get_position(self):
        return self._position
    
    def set_position(self, position):
        self._position = position

    def set_couleur(self, couleur):
        self._couleur = couleur

    def coups_possibles(self, plateau):
        pass


    
        