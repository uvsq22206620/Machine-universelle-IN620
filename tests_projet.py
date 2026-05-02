import unittest 
from code import  Configuration, MT, init_mt, config_init, pas_calcul, simulation, affiche_config, MT_uni, MT_conversion, MT_uni_3b, MT_uni_4b


class TestQ1(unittest.TestCase):
    def test(self):
        mt = MT(
            alphabet = ['0', '1'],
            alphabet_travail = ['0', '1', '_'],
            transition = {},
            etat_init = "q0",
            etat_final = "qf",
            nb_rubans = 1
        )
        print("\n")
        print(f"alphabet : {mt.alphabet}")
        print(f"alphabet de travail : {mt.alphabet_travail}")
        print(f"transitions : {mt.transition}")
        print(f"état initial : {mt.etat_init}")        
        print(f"état final : {mt.etat_final}")
        print(f"nombre de rubans : {mt.nb_rubans} ")
        self.assertEqual(mt.etat_init, "q0")
        self.assertEqual(mt.etat_final, "qf")
        self.assertEqual(mt.nb_rubans, 1)
    
    def test_config(self):
        config = Configuration(
            etat = "q0",
            positions = [0],
            rubans = [['a', 'b']]
        )
        print("\n")
        print(f"état : {config.etat}")        
        print(f"position : {config.positions}")
        print(f"rubans : {config.rubans} ")
        self.assertEqual(config.etat, "q0")
        self.assertEqual(config.positions, [0])
        self.assertEqual(config.rubans, [['a', 'b']])

class TestQ2(unittest.TestCase):
    def test_init_mt(self):
        machine = init_mt("division3.txt")
        print("\n")
        print(f"état initial : {machine.etat_init}")        
        print(f"état final : {machine.etat_final}")
        self.assertIsNotNone(machine.etat_init)
        self.assertIsNotNone(machine.etat_final)

    def test_config_init(self):
        machine = init_mt("division3.txt")
        config = config_init(machine, "110")
        print("\n")
        print(f"état : {config.etat}")        
        print(f"position : {config.positions}")
        print(f"rubans : {config.rubans} ")
        self.assertEqual(config.etat, machine.etat_init)
        self.assertEqual(config.positions[0], 0)
        self.assertEqual(config.rubans[0], ['1', '1', '0'])       


class TestQ3(unittest.TestCase):
    def test_pas_calcul(self):
        machine = init_mt("division3.txt")
        config = config_init(machine, "110")
        print("\n")
        print(f"configuration : {config}")
        config_suivante = pas_calcul(machine, config)
        print(f"configuration suivante : {config_suivante}")
        self.assertIsNotNone(config_suivante)


class TestQ4(unittest.TestCase):
    def test_simulation_accepte(self):
        machine = init_mt("division3.txt")
        accepte, historique = simulation("110", machine)
        print(f"nombre d'étapes: {len(historique)}")
        self.assertTrue(accepte)
    
    def test_simulation_rejette(self):
        machine = init_mt("division3.txt")
        accepte, historique = simulation("1", machine)
        print(f"nombre d'étapes: {len(historique)}")
        self.assertFalse(accepte)

class TestQ5(unittest.TestCase):
    def test_affiche_config(self):
        machine = init_mt("division3.txt")
        accepte, historique = simulation("110", machine)
        print("\n")
        try:
            affiche_config(historique)
            print(f"nombre d'étapes: {len(historique)}")
        except Exception:
            self.fail("affiche_config() ne doit pas lever une exception")

class TestQ6(unittest.TestCase):
    def test_comparaison_entiers(self):
        machine = init_mt("comparaison_entiers.txt")
        accepte1, _ = simulation("1#11", machine)
        self.assertTrue(accepte1, "1#11 : 1 < 3, true")
    
    #def test_comparaison_entiers_rejet(self):
    #    machine = init_mt("comparaison_entiers.txt")
    #    accepte2, _ = simulation("11#1", machine)
    #    self.assertFalse(accepte2, "11#1 : 2 >= 1, boucle")

    def test_recherche_liste(self):
        machine = init_mt("rech_liste.txt")
        accepte1, _ = simulation("11#1", machine)
        self.assertTrue(accepte1, "11#1 : 1, true")

    #def test_recherche_liste_rejet(self):
    #    machine = init_mt("rech_liste.txt")
    #    accepte2, _ = simulation("0#1", machine)
    #    self.assertFalse(accepte2, "0#1 : 1, boucle")

    def test_multiplication(self):
        machine = init_mt("mult_unaire.txt")
        accepte, _ = simulation("11#11", machine)
        self.assertTrue(accepte, "sortie = 1111")

class TestQ7(unittest.TestCase):
    def test_uni_type(self):
        resultat = MT_uni("division3.txt")
        self.assertIsInstance(resultat, str)
    
    def test_uni_contient_pipe(self):
        resultat = MT_uni("division3.txt")
        self.assertIn("|", resultat)
    
    def test_uni_commence_par_0(self):
        resultat = MT_uni("division3.txt")
        self.assertTrue(resultat.startswith("0"))

class TestQ8(unittest.TestCase):
    def test_conversion_binaire(self):
        code, binaire, entier = MT_conversion("division3.txt")
        self.assertIsInstance(binaire, str)
    
    def test_conversion_que_01(self):
        code, binaire, entier = MT_conversion("division3.txt")
        self.assertTrue(all(c in "01" for c in binaire))
    
    def test_conversion_entier(self):
        code, binaire, entier = MT_conversion("division3.txt")
        self.assertIsInstance(entier, int)

class TestQ9(unittest.TestCase):
    def test_accepte(self):
        code = MT_uni("echange_bits.txt")
        accepte, _ = MT_uni_3b(code + "#010")
        self.assertTrue(accepte)
    
    def test_historique(self):
        code = MT_uni("echange_bits.txt")
        accepte, historique = MT_uni_3b(code + "#010")
        self.assertGreater(len(historique), 0)  

class TestQ10(unittest.TestCase):
    def test_accepte_avec_assez_detapes(self):
        code = MT_uni("echange_bits.txt")
        accepte, _ = MT_uni_4b(code + "#010#5")  # 5 étapes devraient être suffisantes
        self.assertTrue(accepte)
    
    def test_refuse_avec_trop_peu_detapes(self):
        code = MT_uni("echange_bits.txt")
        accepte, _ = MT_uni_4b(code + "#010#3")  # 3 étapes ne devraient pas être suffisantes
        self.assertFalse(accepte)

if __name__ =='__main__':
    unittest.main(verbosity=2)