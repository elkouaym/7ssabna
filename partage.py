"""Calcul local des remboursements d'une sortie en dirhams."""
import argparse
import json
import re
from collections import Counter
from pathlib import Path


def centimes(valeur):
    if not isinstance(valeur, str) or not re.fullmatch(r"[0-9]+(?:[.,][0-9]{1,2})?", valeur):
        raise ValueError("Montant attendu entre guillemets, avec au plus deux décimales.")
    entier, _, fraction = valeur.replace(",", ".").partition(".")
    montant = int(entier) * 100 + int(fraction.ljust(2, "0"))
    if montant <= 0:
        raise ValueError("Le montant doit être positif.")
    return montant


def nom_valide(nom):
    return isinstance(nom, str) and bool(nom.strip()) and nom == nom.strip()


def bilan(depenses):
    if not isinstance(depenses, list) or not depenses:
        raise ValueError("La liste des dépenses doit contenir au moins un ticket.")
    avances, parts, arrondis = Counter(), Counter(), Counter()
    for numero, ticket in enumerate(depenses, 1):
        try:
            payeur = ticket["paye_par"]
            membres = ticket["pour"]
            montant = centimes(ticket["dh"])
            if not nom_valide(payeur) or not isinstance(membres, list) or not membres:
                raise ValueError("Payeur et participants requis.")
            if not all(map(nom_valide, membres)) or len(set(membres)) != len(membres):
                raise ValueError("Chaque participant doit avoir un nom unique sur le ticket.")
        except (KeyError, TypeError, ValueError) as erreur:
            raise ValueError(f"Ticket {numero} invalide : {erreur}") from erreur
        avances[payeur] += montant
        base, reste = divmod(montant, len(membres))
        # Alterner les centimes indivisibles parmi les participants concernés.
        ordre = sorted(membres, key=lambda nom: (arrondis[nom], nom))
        for rang, nom in enumerate(ordre):
            extra = int(rang < reste)
            parts[nom] += base + extra
            arrondis[nom] += extra
    noms = sorted(set(avances) | set(parts))
    return {nom: (avances[nom], parts[nom]) for nom in noms}


def remboursements(comptes):
    dettes, credits = [], []
    for nom, (avance, part) in sorted(comptes.items()):
        solde = avance - part
        if solde < 0:
            dettes.append([nom, -solde])
        elif solde > 0:
            credits.append([nom, solde])
    mouvements = []
    i = j = 0
    while i < len(dettes) and j < len(credits):
        montant = min(dettes[i][1], credits[j][1])
        mouvements.append((dettes[i][0], credits[j][0], montant))
        dettes[i][1] -= montant
        credits[j][1] -= montant
        i += dettes[i][1] == 0
        j += credits[j][1] == 0
    return mouvements


def dh(montant):
    return f"{montant // 100},{montant % 100:02d} DH"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tickets", type=Path)
    args = parser.parse_args()
    try:
        comptes = bilan(json.loads(args.tickets.read_text(encoding="utf-8-sig")))
    except (ValueError, OSError) as erreur:
        parser.exit(2, f"Erreur : {erreur}\n")
    for nom, (avance, part) in comptes.items():
        print(f"{nom} | avancé {dh(avance)} | part {dh(part)}")
    mouvements = remboursements(comptes)
    for source, cible, montant in mouvements:
        print(f"{source} -> {cible} : {dh(montant)}")
    if not mouvements:
        print("Tout est équilibré.")


if __name__ == "__main__":
    main()
