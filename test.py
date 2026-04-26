class Configuration : 
    def __init__(self, etat, positions, rubans):
        self.etat = etat
        self.positions = positions  # liste de positions (une par ruban)
        self.rubans = rubans  # liste de rubans

    def __str__(self):
        return f"Etat : {self.etat}, Positions : {self.positions}, Rubans : {self.rubans}"
    
class MT:
    def __init__(self, alphabet, alphabet_travail, transition, etat_init, etat_final, nb_rubans=1):
        self.alphabet = alphabet
        self.alphabet_travail = alphabet_travail
        self.transition = transition
        self.etat_init = etat_init
        self.etat_final = etat_final
        self.nb_rubans = nb_rubans


def init_mt(nom_fichier): #question 2

    with open(nom_fichier, "r") as fichier:
        lignes = fichier.readlines()
    
    lignes_propres = [] #récupération des lignes qui ne sont ni des coms ni des lignes vides
    for ligne in lignes:
        # Enlever les commentaires inline
        if "//" in ligne:
            ligne = ligne[:ligne.index("//")]
        ligne = ligne.strip()
        if not ligne:
            continue
        lignes_propres.append(ligne)
    
    etat_init = None #extraction de l'état initial et de l'état final
    etat_final = None
    
    for ligne in lignes_propres: #on parcourt les lignes pour trouver init/accept et on stocke dans des variables
        if ligne.startswith("init:"):
            etat_init = ligne.split(":")[1].strip()
        elif ligne.startswith("accept:"):
            etat_final = ligne.split(":")[1].strip()
    
    transitions = {} #dico de transitions
    i = 0
    nb_rubans = None  # détection automatique du nombre de rubans
    
    while i < len(lignes_propres):
        ligne = lignes_propres[i]
        
        if ligne.startswith("name:") or ligne.startswith("init:") or ligne.startswith("accept:"):
            i += 1
            continue
        
        if "," in ligne: #si la ligne contient une virgule, c'est une ligne de transition
            partie_lue = ligne.split(",")
            
            # Déterminer nb_rubans à partir de la première transition valide
            if nb_rubans is None:
                nb_rubans = len(partie_lue) - 1
            
            if len(partie_lue) == nb_rubans + 1:
                etat = partie_lue[0].strip()
                symboles_lus = tuple(s.strip() for s in partie_lue[1:])
                
                if i + 1 < len(lignes_propres): #on vérifie qu'il y a une ligne suivante pour la suite de la transition
                    ligne_out = lignes_propres[i + 1]
                    partie_ecrite = ligne_out.split(",")
                    
                    # Format: état_suiv, symboles_écrits (k), directions (k)
                    if len(partie_ecrite) == 2 * nb_rubans + 1:
                        etat_suivant = partie_ecrite[0].strip()
                        symboles_ecrits = [s.strip() for s in partie_ecrite[1:nb_rubans+1]]
                        directions_raw = [d.strip() for d in partie_ecrite[nb_rubans+1:]]
                        
                        directions = []
                        for direction in directions_raw:
                            if direction == ">": #conversion des directions en fonction du format
                                directions.append("R")
                            elif direction == "<":
                                directions.append("L")
                            elif direction == "-":
                                directions.append("-")
                            else:
                                directions.append(direction)
                        
                        # Stocker la transition
                        cle = (etat, symboles_lus)
                        transitions[cle] = (etat_suivant, symboles_ecrits, directions)
                        
                        i += 2
                        continue
        i += 1
    
    if nb_rubans is None:
        nb_rubans = 1
    
    alphabet = set() #creation de l'alphabet et de l'alphabet de travail à partir des transitions
    alphabet_travail = set()
    
    for (etat, symboles_lus), (etat_suivant, symboles_ecrits, directions) in transitions.items():
        for sym in symboles_lus:
            alphabet_travail.add(sym)
        for sym in symboles_ecrits:
            alphabet_travail.add(sym)
    
    alphabet = alphabet_travail.copy() 
    
    return MT( # retourne une instance de la classe MT avec les éléments du fichier
        alphabet=list(alphabet),
        alphabet_travail=list(alphabet_travail),
        transition=transitions,
        etat_init=etat_init,
        etat_final=etat_final,
        nb_rubans=nb_rubans
    )


def config_init(machine, mot): #fonction qui crée la configuration initiale à partir de la machine et du mot d'entrée
    rubans = [list(mot)] + [[] for _ in range(machine.nb_rubans - 1)]
    positions = [0] * machine.nb_rubans
    
    return Configuration( # retourne une instance de la classe Configuration avec l'état initial de la machine, les positions et les rubans
        etat=machine.etat_init,
        positions=positions,
        rubans=rubans
    )


def pas_calcul(machine, configuration): #question 3
    if configuration.etat == machine.etat_final:
        return None
    
    # Créer des copies AVANT de modifier
    nv_rubans = [r.copy() for r in configuration.rubans]
    nv_positions = configuration.positions.copy()
    symboles_lus = []
    
    # Lire sur chaque ruban
    for i in range(machine.nb_rubans):
        pos = nv_positions[i]
        ruban = nv_rubans[i]
        
        # Étendre le ruban
        while pos >= len(ruban):
            ruban.append('_')
        if pos < 0:
            ruban.insert(0, '_')
            nv_positions[i] += 1
            pos = nv_positions[i]  # ✅ CORRECTION : relire à la nouvelle position
        
        symboles_lus.append(ruban[pos])
    
    # Créer la clé de transition
    cle = (configuration.etat, tuple(symboles_lus))
    
    if cle not in machine.transition:
        return None

    etat_suivant, symboles_ecrits, directions = machine.transition[cle]

    # Écrire et déplacer les têtes
    for i in range(machine.nb_rubans):
        if nv_positions[i] < len(nv_rubans[i]):
            nv_rubans[i][nv_positions[i]] = symboles_ecrits[i]
        
        nv_pos = nv_positions[i]
        if directions[i] == "R":
            nv_positions[i] = nv_pos + 1
        elif directions[i] == "L":
            nv_positions[i] = nv_pos - 1

    return Configuration(
        etat=etat_suivant,
        positions=nv_positions,
        rubans=nv_rubans
    )

def simulation(mot, machine): #question 4
    configuration = config_init(machine, mot) 
    historique = [configuration]

    if configuration.etat == machine.etat_final:
        return True, historique

    while configuration.etat != machine.etat_final:
        configuration_suivante = pas_calcul(machine, configuration)

        if configuration_suivante is None:
            return False, historique
        
        configuration = configuration_suivante
        historique.append(configuration)

    return True, historique

def affiche_config(configurations): #question 5
    for i in range(len(configurations)):
        config = configurations[i]
        print(f"étape {i} : {config}")

