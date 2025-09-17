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
    while True:
        try:
            val = input("Selectionnez une case (ligne,col): ")
            # Autoriser les espaces ou virgules
            val = val.replace(" ", ",")
            x, y = map(int, val.split(","))
            
            # Vérification des bornes
            if 0 <= x < TAILLE and 0 <= y < TAILLE:
                return x, y
            else:
                print("Coordonnées hors de la grille ! Entrez des valeurs entre 0 et 4.")
        
        except ValueError:
            print("Format invalide ! Entrez les coordonnées sous la forme 'ligne,col' (ex: 0,2 ou 1 3).")


def jouer():
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

    print("\Bravo! Vous avez coule tous les bateaux!")
    affiche_grille(grille)

if __name__ == "__main__":
    jouer()
