class Jeu:

    def __init__(self, tour_actuel):
        self.__tour_actuel = tour_actuel
        self.__historique_coups = []
        self.__partie_terminee = False

    def lancer_partie(self):
        pass

    def tour_joueur(self):
        pass

    def verifier_valide_coup(self, pos_dep, pos_arr):
        pass

    def effectuer_coup(self, pos_dep, pos_arr):
        pass

    def verifier_echec_et_mat(self, couleur):
        pass

    def get_tour_actuel(self):
        return self.__tour_actuel
    
    def set_tour_actuel(self, tour):
        self.__tour_actuel = tour

    def get_historique_coups(self):
        return self.__historique_coups
    
    def ajouter_coup_historique(self, coup):
        self.__historique_coups.append(coup)

    def get_partie_terminee(self):
        return self.__partie_terminee
    
    def set_partie_terminee(self, val):
        self.__partie_terminee = val