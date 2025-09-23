"""
Module bataille_navale
Ce module implémente un jeu de bataille navale simple en Python.
"""

import random

# Constantes globales
TAILLE_MIN = 3  # Taille minimale autorisée pour la grille
TAILLE_MAX = 10  # Taille maximale autorisée pour la grille
NB_BATEAUX = 3  # Nombre de bateaux à placer sur la grille

def creer_grille(taille):
    """
    Crée une grille vide de taille donnée.
    :param taille: Taille de la grille (entier).
    :return: Grille sous forme de liste de listes.
    """
    return [["~"] * taille for _ in range(taille)]

def afficher_grille(grille):
    """
    Affiche la grille en masquant les bateaux.
    :param grille: Grille à afficher.
    """
    for ligne in grille:
        print(" ".join("~" if case == "B" else case for case in ligne))
    print()

def placer_bateaux(grille, nombre_bateaux):
    """
    Place un nombre donné de bateaux aléatoirement sur la grille.
    :param grille: Grille où placer les bateaux.
    :param nombre_bateaux: Nombre de bateaux à placer.
    :return: Liste des positions des bateaux.
    """
    bateaux = []
    taille_grille = len(grille)
    while len(bateaux) < nombre_bateaux:
        x = random.randint(0, taille_grille - 1)
        y = random.randint(0, taille_grille - 1)
        if grille[x][y] == "~":
            grille[x][y] = "B"
            bateaux.append((x, y))
    return bateaux

def demander_taille_grille():
    """
    Demande à l'utilisateur de choisir la taille de la grille.
    - Vérifie que l'entrée est un entier.
    - Vérifie que la taille est dans les limites définies.
    :return: Taille de la grille (entier).
    """
    while True:
        try:
            taille = int(input(f"Entrez la taille de la grille ({TAILLE_MIN}-{TAILLE_MAX}): "))
            if TAILLE_MIN <= taille <= TAILLE_MAX:
                return taille
            print(f"Erreur: La taille doit être entre {TAILLE_MIN} et {TAILLE_MAX}.")
        except ValueError:
            print("Erreur: Veuillez entrer un nombre entier valide.")

def demander_coordonnees():
    """
    Demande à l'utilisateur de choisir une case.
    :return: Coordonnées choisies (x, y).
    """
    while True:
        try:
            val = input("Sélectionnez une case (ligne,col): ")
            x, y = map(int, val.split(","))
            return x, y
        except ValueError:
            print("Entrée invalide. Veuillez entrer deux nombres séparés par une virgule (ex: 1,2)")

def jouer():
    """
    Fonction principale pour jouer à la bataille navale.
    """
    print("Bienvenue à la bataille navale!")

    # Demander la taille de la grille à l'utilisateur
    taille = demander_taille_grille()

    # Créer la grille et placer les bateaux
    grille = creer_grille(taille)
    placer_bateaux(grille, NB_BATEAUX)

    nb_succes = 0
    while nb_succes < NB_BATEAUX:
        print("Grille:")
        afficher_grille(grille)

        try:
            x, y = demander_coordonnees()

            # Vérifier si les coordonnées sont valides
            if not (0 <= x < taille and 0 <= y < taille):
                print("Coordonnées hors limites. Réessayez.")
                continue

            if grille[x][y] == "B":
                print("Touché!")
                grille[x][y] = "X"
                nb_succes += 1
            elif grille[x][y] == "~":
                print("Raté!")
                grille[x][y] = "O"
            else:
                print("Vous avez déjà tiré ici. Réessayez.")
        except IndexError:
            print("Coordonnées invalides. Réessayez.")

    print("\nBravo! Vous avez coulé tous les bateaux!")
    afficher_grille(grille)

if __name__ == "__main__":
    jouer()
