class Configuration : 
    def __init__(self, etat, pos, ruban):
        self.etat = etat
        self.pos = pos
        self.ruban = ruban

class MachineTuring:
    def __init__(self, alphabet, transition, etat_init, etat_final):
        self.alphabet = alphabet
        self.transition = transition
        self.etat_init = etat_init
        self.etat_final = etat_final

    def lecture(self):
        with open("division3.txt", "r") as fichier : 
            lignes = fichier.readlines()
            ligne_propre = []
            for ligne in lignes:
                ligne = ligne.strip()
                if not ligne:
                    continue
                elif ligne.startswith("//"):
                    continue
                ligne_propre.append(ligne)

            name = None 
            init = None
            accept = None
            for ligne in ligne_propre:
                if ligne.startswith("name:"):
                    name = ligne.split(":")[1].strip()
                elif ligne.startswith("init:"):
                    init = ligne.split(":")[1].strip()
                elif ligne.startswith("accept:"):
                    accept = ligne.split(":")[1].strip()

        transitions = {}
        
        return MachineTuring(
            alphabet=[0,1],
            transition= transitions,
            etat_init= init, 
            etat_final= accept
            )


mt = MachineTuring(
    alphabet=["0","1"], 
    transition={("q0", "0") : ("q1", "1", "R"), ("q0", "0") : ("q0", "1", "R")}, 
    etat_final= "q1", 
    etat_init= "q0")

