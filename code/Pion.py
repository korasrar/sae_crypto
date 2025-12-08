import Piece

class Pion(Piece.Piece):

    def __init__(self, couleur, position, premier_mouvement=False):
        super().__init__(couleur, position)
        self.__premier_mouvement = premier_mouvement

    def get_premier_mouvement(self):
        return self.__premier_mouvement
    
    def coups_possibles(self, plateau):
        return super().coups_possibles(plateau)

        

