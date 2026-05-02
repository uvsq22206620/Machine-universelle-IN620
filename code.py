class Configuration : 
    def __init__(self, etat, positions, rubans):
        self.etat = etat
        self.positions = positions
        self.rubans = rubans

    def __str__(self):
        return f"Etat : {self.etat}, Positions : {self.positions}, Ruban : {self.rubans}"
    
class MT:
    def __init__(self, alphabet, alphabet_travail, transition, etat_init, etat_final, nb_rubans):
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
        ligne = ligne.strip()
        if not ligne or ligne.startswith("//"):
            continue
        lignes_propres.append(ligne)
    
    etat_init = None #extraction de l'état initial et de l'état final
    etat_final = None
    
    for ligne in lignes_propres: #on parcourt les lignes pour trouver init/accept et on stocke dans des variables
        if ligne.startswith("init:"):
            etat_init = ligne.split(":")[1].strip()
        elif ligne.startswith("accept:"):
            etat_final = ligne.split(":")[1].strip()
    
    transitions = {} #dico de transitions, clé = (etat, symbole_lu), valeur = (etat_suivant, symbole_ecrit, direction)
    i = 0
    nb_rubans = None 

    while i < len(lignes_propres): #
        ligne = lignes_propres[i]
        
        if ligne.startswith("name:") or ligne.startswith("init:") or ligne.startswith("accept:"): #on ignore nom, init et accept
            i += 1
            continue
        
        if "," in ligne: #si la ligne contient une virgule, c'est que c'est une ligne de transition
            partie_lue = ligne.split(",") 

            if nb_rubans is None : 
                nb_rubans = len(partie_lue) -1

            if len(partie_lue) == nb_rubans +1:
                etat = partie_lue[0].strip()
                symbole_lu = tuple(s.strip() for s in partie_lue[1:])
                
                if i + 1 < len(lignes_propres): #on vérifie qu'il y a une ligne suivante pour la suite de la transition
                    ligne_out = lignes_propres[i + 1]
                    partie_ecrite = ligne_out.split(",")

                    if len(partie_ecrite) == 2 * nb_rubans + 1 :
                        etat_suivant = partie_ecrite[0].strip()
                        symbole_ecrit = [s.strip() for s in partie_ecrite[1:nb_rubans+1]]
                        direction2base = [d.strip() for d in partie_ecrite[nb_rubans+1:]]


                        directions = []
                        for dir in direction2base:    
                            if dir == ">": #conversion des directions en fonction du format
                                directions.append("R")
                            elif dir == "<":
                                directions.append("L")
                            elif dir == "-":
                                directions.append("-")
                            else:
                                directions.append(dir)
                        
                        cle = (etat, symbole_lu)
                        transitions[cle] = (etat_suivant, symbole_ecrit, directions) 
                        i += 2
                        continue
        i += 1
    if nb_rubans is None: 
        nb_rubans = 1
    
    alphabet = set() #creation de l'alphabet et de l'alphabet de travail à partir des transitions
    alphabet_travail = {'0','1','#','|','_'}
    
    for (etat, symbole_lu), _ in transitions.items(): #on parcourt les transitions, on ajoute les symboles lus/écrits dans les alpabets respectifs
        for sym in symbole_lu:
            if sym != '_':
                alphabet.add(sym)
        
    return MT( # retourne une instance de la classe MT avec les éléments du fichier
        alphabet=list(alphabet),
        alphabet_travail=list(alphabet_travail),
        transition=transitions,
        etat_init=etat_init,
        etat_final=etat_final,
        nb_rubans=nb_rubans
    )


def config_init(machine, mot): #fonction qui crée la configuration initiale à partir de la machine et du mot d'entrée
    rubans = [list(mot)] + [[] for _ in range(machine.nb_rubans -1)]
    positions = [0] * machine.nb_rubans
    
    return Configuration( # retourne une instance de la classe Configuration avec l'état initial de la machine, la position 0 et le ruban avec le mot d'entrée
        etat=machine.etat_init,
        positions=positions,
        rubans=rubans
    )


def pas_calcul(machine, configuration): #question 3
    if configuration.etat == machine.etat_final:
        return None
    
    nv_rubans = [r.copy() for r in configuration.rubans]
    nv_positions = configuration.positions.copy()
    symbole_lu = []

    for i in range(machine.nb_rubans):
        pos = nv_positions[i]
        ruban = nv_rubans[i]

        while pos >= len(ruban):
            ruban.append('_')
        if pos < 0:
            ruban.insert(0,'_')
            nv_positions[i] += 1
            pos = nv_positions[i]

        symbole_lu.append(ruban[pos])

    cle = (configuration.etat, tuple(symbole_lu))
    if cle not in machine.transition:
        return None
    
    etat_suivant, symbole_ecrit, direction = machine.transition[cle]
    
    for i in range(machine.nb_rubans):
        if nv_positions[i] < len(nv_rubans[i]):
            nv_rubans[i][nv_positions[i]] = symbole_ecrit[i]
        
        if direction[i] == "R":
            nv_positions[i] += 1
        elif direction[i] == "L":
            nv_positions[i] -= 1

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
    for i in range (len(configurations)):
        config = configurations[i]
        print(f"étape {i} : {config}")


def MT_uni(nom_fichier): # Q7
    n = init_mt(nom_fichier)

    etats = set() #Collecte des états
    for (etat, _), (etat_suivant,_,_) in n.transition.items():
        etats.add(etat)
        etats.add(etat_suivant)

    mapping = {} # Mapping des états vers des codes binaires
    mapping[n.etat_init] = "0"
    mapping[n.etat_final] = "1"

    compteur = 0
    for etat in etats:
        if etat not in mapping:
            mapping[etat] = bin(compteur)[2:].zfill(2)
            compteur += 1
    
    transition_codees=[] # Liste des transitions codées

    for (etat, symbole_lu), (etat_suivant, symbole_ecrit, directions) in n.transition.items():
        etat_code = mapping[etat]
        etat_suivant_code = mapping[etat_suivant]
        sym_lu = symbole_lu[0]
        sym_ecrit = symbole_ecrit[0]
        direction = directions[0]
        if direction == "R":
                direction_codee = ">"
        elif direction == "L":
                direction_codee = "<"
        else:
                direction_codee = "-"
        
        transition_codee = f"{etat_code}|{sym_lu}|{sym_ecrit}|{direction_codee}|{etat_suivant_code}"
        transition_codees.append (transition_codee)
    
    return "|".join(transition_codees)

def MT_conversion(nom_fichier): #Q8
    code = MT_uni(nom_fichier)

    res = ""
    for char in code:
        res += bin(ord(char))[2:].zfill(8) # Convertit chaque caractère en binaire sur 8 bits et les concatène
    
    res_ent = int(res, 2) # Convertit la chaîne de binaire en entier
    return code, res, res_ent

def MT_uni_3b(entree):  # Q9 
    code_m, x = entree.split("#", 1)

    ruban1 = list(code_m)
    ruban2 = list("0")  # état initial
    ruban3 = list(x)

    pos3 = 0  # tête sur ruban 3

    # découpage des transitions
    elements = code_m.split("|")

    transitions = []
    for i in range(0, len(elements), 5):
        transitions.append({
            "etat": elements[i],
            "lu": elements[i+1],
            "ecrit": elements[i+2],
            "dir": elements[i+3],
            "suivant": elements[i+4]
        })

    historique = [] # Liste des config

    while True:
        # Extension du ruban 3 si la tête dépasse les bords
        if pos3 >= len(ruban3):
            ruban3.append('_')
        if pos3 < 0:
            ruban3.insert(0, '_')
            pos3 = 0

        symbole = ruban3[pos3]
        etat = ''.join(ruban2)

        # sauvegarde config
        historique.append(Configuration(
            etat=etat,
            positions=[0, 0, pos3],
            rubans=[ruban1.copy(), ruban2.copy(), ruban3.copy()]
        ))

        # état final
        if etat == "1":
            return True, historique

        # chercher transition
        trouve = False
        for t in transitions:
            if t["etat"] == etat and t["lu"] == symbole:
                trouve = True

                # appliquer
                ruban2 = list(t["suivant"])
                ruban3[pos3] = t["ecrit"]

                if t["dir"] == ">":
                    pos3 += 1
                elif t["dir"] == "<":
                    pos3 -= 1

                break

        if not trouve:
            return False, historique


def MT_uni_4b(entree):  # Q10
    code_m, x, n = entree.split("#", 2)
    n = int(n)
    ruban1 = list(code_m)
    ruban2 = list("0")  # état initial
    ruban3 = list(x)
    ruban4 = list(str(n))  # ruban pour n

    pos3 = 0  # tête sur ruban 3
    pos4 = 0  # tête sur ruban 4

    # découpage des transitions
    elements = code_m.split("|")
    transitions = []
    for i in range(0, len(elements), 5):
        transitions.append({
            "etat": elements[i],
            "lu": elements[i+1],
            "ecrit": elements[i+2],
            "dir": elements[i+3],
            "suivant": elements[i+4]
        })
    historique = [] # Liste des config
    
    while n > 0 :
        # Extension du ruban 3 si la tête dépasse les bords
        if pos3 >= len(ruban3):
            ruban3.append('_')
        if pos3 < 0:
            ruban3.insert(0, '_')
            pos3 = 0

        symbole = ruban3[pos3]
        etat = ''.join(ruban2)

        # sauvegarde config
        historique.append(Configuration(
            etat=etat,
            positions=[0, 0, pos3, pos4],
            rubans=[ruban1.copy(), ruban2.copy(), ruban3.copy(), ruban4.copy()]
        ))

        # état final
        if etat == "1":
            return True, historique

        # chercher transition
        trouve = False
        for t in transitions:
            if t["etat"] == etat and t["lu"] == symbole:
                trouve = True

                # appliquer
                ruban2 = list(t["suivant"])
                ruban3[pos3] = t["ecrit"]

                if t["dir"] == ">":
                    pos3 += 1
                elif t["dir"] == "<":
                    pos3 -= 1

                break

        if not trouve:
            return False, historique
        
        n -= 1
        ruban4 = list(str(n))  # mise à jour du ruban compteur

    return False, historique  # n étapes écoulées sans accepter
    
    









#code = MT_uni("echange_bits.txt")
#accepte, historique = MT_uni_4b(code + "#010#3")
#print("Accepté :", accepte)
#affiche_config(historique)