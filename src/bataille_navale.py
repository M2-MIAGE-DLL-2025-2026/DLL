"""
Module bataille_navale
Ce module implémente un jeu de bataille navale simple en Python.
"""

import random
from typing import List, Tuple

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
    Demande au user de choisir une case.
    Peut aussi saisir 'retry' pour recommencer ou 'exit' pour quitter instead of les coordonnees .
    """
    while True:
        val = input("Sélectionnez une case (ligne,col) ou tapez 'retry' ou 'exit' : ").strip().lower()
        if val == "retry":
            return "retry"
        elif val == "exit":
            return "exit"
        try:
            x, y = map(int, val.split(","))
            return x, y
        except ValueError:
            print("Entrée invalide. Exemple valide : 1,2")


def confirmation_retry_exit(message):
    """demander une confirmation yes/no au user pour quitter(exit) ou recommencer(retry)"""
    while True:
        rep = input(f"{message} (yes/no) : ").strip().lower()
        if rep in ["yes", "y"]:
            return True
        elif rep in ["no", "n"]:
            return False
        else:
            print("Réponse invalide. Tapez 'yes' ou 'no'.")

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
            coord = demander_coordonnees()
            if coord == "retry":
                if confirmation_retry_exit("Voulez-vous vraiment recommencer le jeu?"):
                    return True
                else:
                    continue
            elif coord == "exit":
                if confirmation_retry_exit("Voulez-vous vraiment quitter le jeu?"):
                    print("Merci d'avoir joué! Au revoir! 👋")
                    return False
                else:
                    continue
    
            x, y = coord

            # Vérifier si les coordonnées sont valides
            if not (0 <= x < taille and 0 <= y < taille):
                print("Coordonnées hors limites. Réessayez.")
                continue

            if grille[x][y] == "B":
                print("Touché! 🎯")
                grille[x][y] = "X"
                nb_succes += 1
            elif grille[x][y] == "~":
                print("Raté! ❌")
                grille[x][y] = "O"
            else:
                print("Vous avez déjà tiré ici. Réessayez.")
        except IndexError:
            print("Coordonnées invalides. Réessayez.")

    print("\nBravo! Vous avez coulé tous les bateaux! 🎉")
    afficher_grille(grille)
    
    if confirmation_retry_exit("Voulez-vous rejouer ?"):
        return True
    else:
        return False

def main():
    """boucle principale pour gérer le replay."""
    while True:
        rejouer = jouer()
        if not rejouer:
            break
        
        
if __name__ == "__main__":
    main()
