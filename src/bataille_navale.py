"""Module de jeu Bataille Navale (version simple).

Contient des utilitaires pour créer/afficher une grille, placer des bateaux
et exécuter une boucle de jeu minimale (mode console).
"""

import random
from typing import List, Tuple

TAILLE = 5
NB_BATEAUX = 3


def cree_grille(size: int) -> List[List[str]]:
    """Crée et retourne une grille carrée de taille `size` initialisée à "~".

    Args:
        size: dimension de la grille (nombre de lignes/colonnes).
    """
    return [["~"] * size for _ in range(size)]


def affiche_grille(grille: List[List[str]]) -> None:
    """Affiche la grille dans la console en masquant les bateaux.

    Les cases contenant "B" (bateau) sont affichées comme "~" afin de
    ne pas dévoiler leur position.
    """
    for ligne in grille:
        print(" ".join("~" if case == "B" else case for case in ligne))
    print()


def place_bateaux(grille: List[List[str]], nb_bateaux: int) -> List[Tuple[int, int]]:
    """Place aléatoirement `nb_bateaux` bateaux sur la grille.

    Args:
        grille: matrice préexistante (modifiée en place).
        nb_bateaux: nombre de bateaux à placer.

    Returns:
        Liste des positions (x, y) des bateaux placés.
    """
    bateaux: List[Tuple[int, int]] = []
    size = len(grille)
    while len(bateaux) < nb_bateaux:
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        if grille[x][y] == "~":
            grille[x][y] = "B"
            bateaux.append((x, y))
    return bateaux

def choix_utilisateur() -> Tuple[int, int]:
    """Lit une saisie 'ligne,col'et verif si c'est mal ecrit (x, y)."""
    while True:
        val = input("Selectionnez une case (ligne,col): ")
        try:
            x, y = map(int, val.strip().split(","))
        except ValueError:
            print("Entrée invalide. Utilisez le format 'ligne,col' (ex: 0,1).")
            continue

        if 0 <= x < TAILLE and 0 <= y < TAILLE:
            return x, y

        print(f"Coordonnées hors grille. Valeurs autorisées: 0 à {TAILLE - 1}. Réessayez.")

def jouer() -> None:
    """Boucle de jeu console minimaliste.

    Place des bateaux puis demande des coordonnées tant que tous les
    bateaux n'ont pas été touchés.
    """
    print("Bienvenu a la bataille royale!")

    grille = cree_grille(TAILLE)
    place_bateaux(grille, NB_BATEAUX)

    nb_succes = 0
    while nb_succes < NB_BATEAUX:
        print("Grille:")
        affiche_grille(grille)

        x, y = choix_utilisateur()

        if grille[x][y] == "B":
            print("Touche!")
            grille[x][y] = "X"
            nb_succes += 1
        elif grille[x][y] == "~":
            print("Rate!")
            grille[x][y] = "O"

    print("Bravo ! Vous avez coulé tous les bateaux !")
    affiche_grille(grille)


if __name__ == "__main__":
    jouer()
