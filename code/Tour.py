import Piece

class Tour(Piece.Piece):

    def __init__(self, couleur, position, a_bouge=False):
        super().__init__(couleur, position)
        self.__a_bouge = a_bouge

    def coups_possibles(self, plateau):
        return super().coups_possibles(plateau)
    
    def get_a_bouge(self):
        return self.__a_bouge
    
    def set_a_bouge(self, val):
        self.__a_bouge = val