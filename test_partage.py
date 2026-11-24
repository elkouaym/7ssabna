import json
from pathlib import Path
import unittest
from partage import bilan, centimes, remboursements


class PartageTests(unittest.TestCase):
    def test_sortie(self):
        comptes = bilan(json.loads(Path(__file__).with_name("sortie.json").read_text()))
        self.assertEqual(comptes, {"Nora": (6000, 3200), "Samir": (2400, 3200), "Yasmine": (0, 2000)})
        self.assertEqual(remboursements(comptes), [("Samir", "Nora", 800), ("Yasmine", "Nora", 2000)])

    def test_centimes_alternes(self):
        ticket = {"paye_par": "A", "dh": "0,01", "pour": ["B", "A"]}
        self.assertEqual(bilan([ticket, ticket]), {"A": (2, 1), "B": (0, 1)})

    def test_payeur_exterieur(self):
        comptes = bilan([{"paye_par": "A", "dh": "2", "pour": ["B"]}])
        self.assertEqual(remboursements(comptes), [("B", "A", 200)])

    def test_aucun_remboursement(self):
        self.assertEqual(remboursements({"A": (100, 100)}), [])

    def test_montant_invalide(self):
        with self.assertRaises(ValueError):
            centimes("2.555")

    def test_participant_double(self):
        with self.assertRaises(ValueError):
            bilan([{"paye_par": "A", "dh": "2", "pour": ["B", "B"]}])
