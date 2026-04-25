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
    while i < len(lignes_propres): #
        ligne = lignes_propres[i]
        
        if ligne.startswith("name:") or ligne.startswith("init:") or ligne.startswith("accept:"): #on ignore nom, init et accept
            i += 1
            continue
        
        if "," in ligne: #si la ligne contient une virgule, c'est une ligne de transition
            partie_lue = ligne.split(",") 
            if len(partie_lue) == 2:
                etat = partie_lue[0].strip()
                symbole_lu = partie_lue[1].strip()
                
                if i + 1 < len(lignes_propres): #on vérifie qu'il y a une ligne suivante pour la suite de la transition
                    ligne_out = lignes_propres[i + 1]
                    partie_ecrite = ligne_out.split(",")
                    if len(partie_ecrite) == 3:
                        etat_suivant = partie_ecrite[0].strip()
                        symbole_ecrit = partie_ecrite[1].strip()
                        direction = partie_ecrite[2].strip()
                        
                        if direction == ">": #conversion des directions en fonction du format
                            direction = "R"
                        elif direction == "<":
                            direction = "L"
                        elif direction == "-":
                            direction = "-"
                        
                        transitions[(etat, symbole_lu)] = (etat_suivant, symbole_ecrit, direction) 
                        i += 2
                        continue
        i += 1
    
    alphabet = set() #creation de l'alphabet et de l'alphabet de travail à partir des transitions
    alphabet_travail = set()
    
    for (etat, symbole), (etat_suivant, symbole_ecrit, direction) in transitions.items(): #on parcourt les transitions, on ajoute les symboles lus/écrits dans les alpabets respectifs
        alphabet_travail.add(symbole)
        alphabet_travail.add(symbole_ecrit)
    
    alphabet = alphabet_travail.copy() 
    
    return MT( # retourne une instance de la classe MT avec les éléments du fichier
        alphabet=list(alphabet),
        alphabet_travail=list(alphabet_travail),
        transition=transitions,
        etat_init=etat_init,
        etat_final=etat_final
    )


def config_init(machine, mot): #fonction qui crée la configuration initiale à partir de la machine et du mot d'entrée
    ruban = list(mot)
    
    return Configuration( # retourne une instance de la classe Configuration avec l'état initial de la machine, la position 0 et le ruban avec le mot d'entrée
        etat=machine.etat_init,
        pos=0,
        ruban=ruban
    )


def pas_calcul(machine, configuration): #question 3
    if configuration.etat == machine.etat_final:
        return None
    
    if configuration.pos < 0 or configuration.pos >= len(configuration.ruban):
        symbole_lu = '_'
    else :
        symbole_lu = configuration.ruban[configuration.pos]

    if (configuration.etat, symbole_lu) not in machine.transition:
            return None

    etat_suivant, symbole_ecrit, direction = machine.transition[(configuration.etat, symbole_lu)]

    nv_ruban = configuration.ruban.copy()

    if configuration.pos < len(nv_ruban):
        nv_ruban[configuration.pos] = symbole_ecrit
    
    nv_pos = configuration.pos
    if direction == "R":
        nv_pos += 1
    elif direction == "L":
        nv_pos -= 1

    return Configuration(
        etat=etat_suivant,
        pos=nv_pos,
        ruban=nv_ruban
    )


def simulation(mot, machine): #question 4
    configuration = config_init(machine, mot) 

    if configuration.etat == machine.etat_final:
        return True, historique
    
    historique = [configuration]

    while configuration.etat != machine.etat_final:
        configuration_suivante = pas_calcul(machine, configuration)

        if configuration_suivante is None:
            return False, historique
        
        configuration = configuration_suivante
        historique.append(configuration)

        if configuration.etat == machine.etat_final:
            return True, historique
        else:
            return False, historique


def affiche_config(configurations): #question 5
    for i in range (len(configurations)):
        config = configurations[i]
        print(f"étape {i} : {config}")



machine = init_mt("division3.txt")
accepte, configs = simulation("110", machine)
print(f"Acceptée: {accepte}")
affiche_config(configs)

machine = init_mt("dec2bin.txt")
accepte, configs = simulation("5", machine)
print(f"acceptée : {accepte}")
affiche_config(configs)


# Test rapide Question 4
#machine = init_mt("dec2bin.txt")
#
#print("Test simulation:")
#print(f"simulation('5', machine) = {simulation('5', machine)}")  
#print(f"simulation('8', machine) = {simulation('8', machine)}")  
#print(f"simulation('10', machine) = {simulation('10', machine)}")       
        

# def test_q1():
# def test_q2():
# def test_q3():
# def test_q4():
# def test_q5():