# 7ssabna

Après une sortie, retrouvez qui doit rembourser qui. Chaque ticket a un payeur et sa propre liste de bénéficiaires. Le calcul fonctionne hors ligne en dirhams.

## Démo

Avec Python 3.8 ou plus récent, ouvrez un terminal dans ce dossier.

```sh
python partage.py sortie.json
python -m unittest -v
```

Dans cet exemple fictif, Nora avance 60 DH de taxi pour trois personnes. Samir avance 24 DH d'impressions pour lui et Nora. Samir rembourse 8 DH à Nora et Yasmine lui rembourse 20 DH.

## Votre groupe

Copiez sortie.json et ajoutez une entrée par ticket. Utilisez le même nom, avec la même casse, pour chaque personne. Saisissez le prix entre guillemets, en DH avec zéro, une ou deux décimales. Le point et la virgule sont acceptés. Chaque bénéficiaire figure une seule fois sur son ticket. Le payeur peut avancer une dépense pour d'autres personnes.

Le programme partage chaque ticket à parts égales entre ses bénéficiaires. Les calculs utilisent des centimes entiers. Les centimes indivisibles vont en priorité aux bénéficiaires ayant reçu le moins de centimes supplémentaires sur les tickets précédents, puis par ordre alphabétique. L'ordre des tickets fixe donc le résultat des arrondis. Les remboursements proposés équilibrent les comptes par ordre alphabétique. Le programme affiche les montants à régler. Les paiements se font séparément.

## Inspirations

[Spliit 1.30.0](https://github.com/spliit-app/spliit/releases/tag/1.30.0), publié le 11 octobre 2026, gère les dépenses partagées via une application web sous licence MIT. [Cospend 4.3.0](https://github.com/julien-nc/cospend-nc/releases/tag/v4.3.0), publié le 20 octobre 2026, gère les budgets de groupe dans Nextcloud sous licence AGPL-3.0. Sources consultées le 24 novembre 2026.

7ssabna applique cette idée aux petits tickets en dirhams avec un fichier local et une règle explicite pour répartir les centimes restants. L'implémentation indépendante utilise uniquement les modules fournis avec Python.
