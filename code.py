class Configuration : 
    def __init__(self, etat, pos, ruban):
        self.etat = etat
        self.pos = pos
        self.ruban = ruban

    def __str__(self):
        return f"Etat : {self.etat}, Position : {self.pos}, Ruban : {self.ruban}"
    
class MT:
    def __init__(self, alphabet, alphabet_travail, transition, etat_init, etat_final):
        self.alphabet = alphabet
        self.alphabet_travail = alphabet_travail
        self.transition = transition
        self.etat_init = etat_init
        self.etat_final = etat_final

   