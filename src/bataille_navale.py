"""# Bataille Navale - Version Simple"""

import random

TAILLE = 5
NB_BATEAUX = 3

def cree_grille(size):
    """Crée une grille de taille size x size remplie de '~'."""
    return [["~"] * size for _ in range(size)]

def affiche_grille(grille):
    """Affiche la grille en masquant les bateaux."""
    for ligne in grille:
        print(" ".join("~" if case == "B" else case for case in ligne))
    print()

def place_bateaux(grille, nb_bateaux):
    """Place nb_bateaux bateaux aléatoirement sur la grille."""
    bateaux = []
    while len(bateaux) < nb_bateaux:
        x = random.randint(0, TAILLE - 1)
        y = random.randint(0, TAILLE - 1)
        if grille[x][y] == "~":
            grille[x][y] = "B"
            bateaux.append((x, y))
    return bateaux

def choix_utilisateur():
    """Demande à l'utilisateur de choisir une case."""
    val = input("Selectionnez une case (ligne,col): ")
    x, y = map(int, val.split(","))
    return x, y

def jouer():
    """Fonction principale pour jouer au jeu."""
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

    print("\\Bravo! Vous avez coule tous les bateaux!")
    affiche_grille(grille)

if __name__ == "__main__":
    jouer()
