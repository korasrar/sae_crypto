import Piece

class Dame(Piece.Piece):
    def __init__(self, couleur, position):
        super().__init__(couleur, position)

    def coups_possibles(self, plateau):
        return super().coups_possibles(plateau)