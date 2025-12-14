import chess
import os


class menu():

    def __init__(self, jeu):
        self.jeu = jeu

    def affichage_menu_principal(self):
        print("1: Partie Locale")
        print("2: Partie en ligne")
        print("3: Historique des parties")
        print("4: quitter")

    def launch(self):
        self.affichage_menu_principal()
        quit = False
        while not quit:
            choice = input("Choisissez une option \n")

            match choice:
                case "1":
                    self.jeu.chess_game()
                case "2":
                    print("Fonctionnalité à implementer")
                case "3":
                    print("Fonctionnalité à implementer")
                case "4":
                    break
        print("fermeture du jeu...")


class Jeu():

    def __init__(self):
        self.board = chess.Board()

    def affiche_plateau(self):
        print(self.board.unicode())

    def reset_plateau(self):
        self.board = chess.Board()

    def a_qui_de_jouer(self, board: chess.Board) -> str:
        print("c'est aux Blancs de jouer" if board.
              turn else "c'est aux Noirs de jouer")

    def display_end_game(self, board: chess.Board):
        outcome = board.outcome()
        if outcome:
            if outcome.winner == chess.WHITE:
                print("Les Blancs ont gagnés")
            elif outcome.winner == chess.BLACK:
                print("Les noirs ont gagnés")
            else:
                print("Match nul")

    def chess_game(self):
        while not self.board.is_game_over():

            self.affiche_plateau()
            self.a_qui_de_jouer(self.board)
            try:
                move = Joueur.move_piece()
                move.strip()
                validator = chess.Move.from_uci(move)

                while validator not in self.board.legal_moves:
                    self.affiche_plateau()
                    print("Ceci est un mouvement illegal")
                    move = input("Un mouvement légal : ")
                    validator = chess.Move.from_uci(move)
                    if validator in self.board.legal_moves:
                        break

                self.board.push_san(move)
            except chess.InvalidMoveError:
                print("Veuillez entrez un mouvement valide")
        self.display_end_game(self.board)
        self.reset_plateau()
        Joueur.revenge()


class Joueur():

    def __init__(self, username):
        self.username = username

    def move_piece() -> str:
        move = input("Entrez un mouvement (a2a3 ou a2 a3) \n")
        return move

    def revenge():
        print("Prendre une revanche ? O/N")
        take_revenge = input().lower()
        match take_revenge:
            case "o":
                os.system('cls' if os.name == 'nt' else 'clear')
                Jeu().chess_game()
            case "n":
                app.launch()


#board.set_fen("rn1qkbnr/pPpb1ppp/4p3/8/3p4/8/PP1PPPPP/RNBQKBNR w KQkq - 1 5") #Position to try to promote "b7a8"

#g2g4
#e7e5
#f2f3
#d8h4

if __name__ == "__main__":
    app = menu(Jeu())
    app.launch()
