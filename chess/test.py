import chess

board = chess.Board()

#board.set_fen("rn1qkbnr/pPpb1ppp/4p3/8/3p4/8/PP1PPPPP/RNBQKBNR w KQkq - 1 5") #Position to try to promote "b7a8"

def affichage_menu_principal():
    print("1: Partie Locale")
    print("2: Partie en ligne")
    print("3: Historique des parties")
    print("4: quitter")

def menu():
    affichage_menu_principal()
    quit = False
    while not quit:
        choice = input("Choisissez une option \n")
        
        match choice:
            case "1":
                chess_game()
            case "2":
                print("Fonctionnalité à implementer")
            case "3":
                print("Fonctionnalité à implementer")
            case "4":
                break
    print("fermeture du jeu...")
    
def a_qui_de_jouer(board: chess.Board)->str:
    return "c'est aux Blancs de jouer" if board.turn else "c'est aux Noirs de jouer"

def chess_game():
    while not board.is_game_over():

        print(board)
        print(a_qui_de_jouer(board))
        try:
            move = input("Entrez un mouvement \n")
            validateur = chess.Move.from_uci(move)

            while validateur not in board.legal_moves:
                print(board)
                print ("C'est pas très légal tout ça REESSAYER")
                move = input("un mouvement légal svp :) : ")
                validateur = chess.Move.from_uci(move)
                if validateur in board.legal_moves:
                    break        

            board.push_san(move)
            print(board)
            print(board.outcome())
        except chess.InvalidMoveError:
            print("Veuillez entrez un mouvement valide")
        
    
if __name__ == "__main__":
    menu()
#board.outcome() -> vérifie si partie terminée ou non

