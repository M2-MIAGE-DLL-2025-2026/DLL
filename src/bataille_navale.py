import random

TAILLE = 5
NB_BATEAUX = 3

def cree_grille(size):
    return [["~"] * size for _ in range(size)]

def affiche_grille(grille):
    for ligne in grille:
        print(" ".join("~" if case == "B" else case for case in ligne))
    print()

def place_bateaux(grille, NB_BATEAUX):
    bateaux = []
    while len(bateaux) < NB_BATEAUX:
        x = random.randint(0, TAILLE - 1)
        y = random.randint(0, TAILLE - 1)
        if grille[x][y] == "~":
            grille[x][y] = "B"
            bateaux.append((x, y))
    return bateaux

def choix_utilisateur():
    val = input("Selectionnez une case (ligne,col): ")
    x, y = map(int, val.split(","))
    return x, y

def jouer():
    print("Bienvenu a la bataille royale!")

    grille = cree_grille(TAILLE)
    place_bateaux(grille, NB_BATEAUX)

    nb_succes = 0
    nb_tir = 0

    while nb_succes < NB_BATEAUX:
        print("Grille:")
        affiche_grille(grille)

        x, y = choix_utilisateur()
        nb_tir = nb_tir+1

        if grille[x][y] == "B":
            print("Touche!")
            grille[x][y] = "X"
            nb_succes += 1
        elif grille[x][y] == "~":
            print("Rate!")
            grille[x][y] = "O"

    print("\Bravo! Vous avez coule tous les bateaux!")
    print (f"\Vous avez tiré {nb_tir} durant la partie")
    affiche_grille(grille)

if __name__ == "__main__":
    jouer()
