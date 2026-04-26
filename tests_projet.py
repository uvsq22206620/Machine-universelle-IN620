import unittest 
from code import  Configuration, MT, init_mt, config_init, pas_calcul, simulation, affiche_config

class TestQ1(unittest.TestCase):
    def test_MT(self):
        mt = MT(
            alphabet = ['0', '1'],
            alphabet_travail = ['0', '1', '_'],
            transition = {},
            etat_init = "q0",
            etat_final = "qf",
            nb_rubans = 1
        )
        self.assertEqual(mt.etat_init, "q0")
        self.assertEqual(mt.etat_final, "qf")
        self.assertEqual(mt.nb_rubans, 1)
    
    def test_config(self):
        config = Configuration(
            etat = "q0",
            positions = [0],
            rubans = [['a', 'b']]
        )
        self.assertEqual(config.etat, "q0")
        self.assertEqual(config.positions, [0])
        self.assertEqual(config.rubans, [['a', 'b']])

class TestQ2(unittest.TestCase):
    def test_init_mt(self):
        machine = init_mt("division3.txt")
        self.assertIsNotNone(machine.etat_init)
        self.assertIsNotNone(machine.etat_final)

    def test_config_init(self):
        machine = init_mt("division3.txt")
        config = config_init(machine, "110")
        self.assertEqual(config.etat, machine.etat_init)
        self.assertEqual(config.positions[0], 0)
        self.assertEqual(config.rubans[0], ['1', '1', '0'])       


class TestQ3(unittest.TestCase):
    def test_pas_calcul(self):
        machine = init_mt("division3.txt")
        config = config_init(machine, "110")
        config_suivante = pas_calcul(machine, config)
        self.assertIsNotNone(config_suivante)


class TestQ4(unittest.TestCase):
    def test_simulation_accepte(self):
        machine = init_mt("division3.txt")
        accepte, historique = simulation("110", machine)
        self.assertTrue(accepte)
    
    def test_simulation_rejette(self):
        machine = init_mt("division3.txt")
        accepte, historique = simulation("1", machine)
        self.assertFalse(accepte)

class TestQ5(unittest.TestCase):
    def test_affiche_config(self):
        machine = init_mt("division3.txt")
        accepte, historique = simulation("110", machine)
        try:
            affiche_config(historique)
        except Exception:
            self.fail("affiche_config() ne doit pas lever d'exception")

class TestQ6(unittest.TestCase):
    def test_comparaison_entiers(self):
        machine = init_mt("comparaison_entiers.txt")
        accepte1, _ = simulation("1#11", machine)
        self.assertTrue(accepte1, "1#11 : 1 < 3 devrait être accepté")
    
    def test_comparaison_entiers_rejet(self):
        machine = init_mt("comparaison_entiers.txt")
        accepte2, _ = simulation("11#1", machine)
        self.assertFalse(accepte2, "11#1 : 2 >= 1 devrait être rejeté")

    def test_recherche_liste(self):
        machine = init_mt("rech_liste.txt")
        # accepte si l'élément est trouvé
        accepte1, _ = simulation("11#1", machine)
        self.assertTrue(accepte1, "11#1 : 1 trouvé devrait être accepté")

    def test_recherche_liste_rejet(self):
        machine = init_mt("rech_liste.txt")
        accepte2, _ = simulation("0#1", machine)
        self.assertFalse(accepte2, "0#1 : 1 non trouvé devrait être rejeté")

if __name__ =='__main__':
    unittest.main()