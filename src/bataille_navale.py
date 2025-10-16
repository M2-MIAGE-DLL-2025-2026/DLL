"""
Module bataille_navale
Ce module implémente un jeu de bataille navale simple en Python.
"""

import random
from typing import Tuple

# Constantes globales
TAILLE_MIN = 3  # Taille minimale autorisée pour la grille
TAILLE_MAX = 10  # Taille maximale autorisée pour la grille
NB_BATEAUX = 3  # Nombre de bateaux à placer sur la grille
HISTORIQUE_PARTIE = []

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


def demander_coordonnees(taille: int = TAILLE_MAX) -> Tuple[int, int]:
    """Lit et retourne une saisie utilisateur au format "ligne,col".

    Valide que les coordonnées sont au bon format et dans les limites de la grille.
    Redemande une saisie tant que l'entrée n'est pas valide.
    Args:
        taille: taille de la grille pour valider les limites (par défaut: TAILLE)
    Returns:
    Un tuple (x, y) contenant les coordonnées saisies par l'utilisateur.
    Peut aussi saisir 'retry' pour recommencer ou 'exit' pour quitter instead of les coordonnees .
    """
    while True:
        val = input("Sélectionnez une case ligne,col ou 'retry' ou 'exit' : ").strip().lower()
        if val in ("retry", "exit"):
            return val
        # Extraire et convertir les valeurs
        try:
            x, y = map(int, val.split(","))
            # Vérifier les limites
            if x < 0 or x >= taille or y < 0 or y >= taille:
                print(f"Coordonnées hors limites! Entrez des valeurs entre 0 et {taille-1}")
                continue
            return x, y
        except ValueError:
            print("Entrée invalide. Veuillez entrer deux nombres séparés par une virgule (ex: 1,2)")

def confirmation_retry_exit(message):
    """Demande une confirmation yes/no au user pour quitter(exit) ou recommencer(retry) le jeu.
    Args:
        message: message à afficher pour la confirmation.
    Returns:
        True si l'utilisateur confirme (yes), False sinon (no).
    """
    while True:
        rep = input(f"{message} (yes/no) : ").strip().lower()
        if rep in ["yes", "y"]:
            return True
        if rep in ["no", "n"]:
            return False
        print("Réponse invalide. Tapez 'yes' ou 'no'.")

def enregistrer_partie(taille, nb_bateaux, nb_succes, nb_tirs):
    """
    Enregistre les résultats d'une partie.
    """
    partie = {
        "taille": taille,
        "bateaux": nb_bateaux,
        "touches": nb_succes,
        "tirs_total": nb_tirs
    }
    HISTORIQUE_PARTIE.append(partie)

def afficher_stats():
    if not HISTORIQUE_PARTIE:
        print("Aucune partie jouée.")
        return
    print("\nStatistiques :")
    for i, partie in enumerate(HISTORIQUE_PARTIE, 1):
        print(f"Partie {i}: Grille {partie['taille']}x{partie['taille']}, "
              f"Bateaux: {partie['bateaux']}, Touchés: {partie['touches']}, "
              f"Tirs: {partie['tirs_total']}")

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
    nb_tirs = 0
    while nb_succes < NB_BATEAUX:
        print("Grille:")
        afficher_grille(grille)

        try:
            coord = demander_coordonnees()
            if coord == "retry":
                if confirmation_retry_exit("Voulez-vous vraiment recommencer le jeu?"):
                    return True
                continue
            if coord == "exit":
                if confirmation_retry_exit("Voulez-vous vraiment quitter le jeu?"):
                    print("Merci d'avoir joué! Au revoir! 👋")
                    return False
                continue
            x, y = coord

            # Vérifier si les coordonnées sont valides
            if not (0 <= x < taille and 0 <= y < taille):
                print("Coordonnées hors limites. Réessayez.")
                continue

            nb_tirs += 1
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
    
    enregistrer_partie(taille, NB_BATEAUX, nb_succes, nb_tirs)
    afficher_stats()
    afficher_grille(grille)
    if confirmation_retry_exit("Voulez-vous rejouer ?"):
        return True
    return False

def main():
    """boucle principale pour gérer le replay."""
    while True:
        rejouer = jouer()
        if not rejouer:
            break


if __name__ == "__main__":
    main()
