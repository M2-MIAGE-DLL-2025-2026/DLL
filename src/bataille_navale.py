"""
Module bataille_navale
Ce module implémente un jeu de bataille navale simple en Python.
"""

import random
import json
import os
from typing import Tuple

# Constantes globales
TAILLE_MIN = 3  # Taille minimale autorisée pour la grille
TAILLE_MAX = 10  # Taille maximale autorisée pour la grille
NB_BATEAUX = 3  # Nombre de bateaux à placer sur la grille
FICHIER_SAUVEGARDE = "sauvegarde_partie.json"  # Nom du fichier de sauvegarde

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
            print("Entrée invalide. Exemple valide : 1,2")


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


def sauvegarder_partie(grille, bateaux, nb_coules, taille):
    """
    Sauvegarde l'état actuel de la partie dans un fichier JSON.
    :param grille: État actuel de la grille.
    :param bateaux: Liste des positions des bateaux.
    :param nb_coules: Nombre de bateaux coulés.
    :param taille: Taille de la grille.
    """
    try:
        donnees = {
            "grille": grille,
            "bateaux": bateaux,
            "nb_coules": nb_coules,
            "taille": taille,
        }
        with open(FICHIER_SAUVEGARDE, "w", encoding="utf-8") as fichier:
            json.dump(donnees, fichier, indent=2)
    except (OSError, IOError) as e:
        print(f"Erreur lors de la sauvegarde: {e}")


def charger_partie():
    """
    Charge une partie sauvegardée depuis le fichier JSON.
    :return: Tuple (grille, bateaux, nb_coules, taille) ou None si échec.
    """
    if not os.path.exists(FICHIER_SAUVEGARDE):
        return None

    try:
        with open(FICHIER_SAUVEGARDE, "r", encoding="utf-8") as fichier:
            donnees = json.load(fichier)

        # Vérifier que toutes les clés nécessaires sont présentes
        cles_requises = ["grille", "bateaux", "nb_coules", "taille"]
        if not all(cle in donnees for cle in cles_requises):
            print("Fichier de sauvegarde invalide (clés manquantes).")
            return None

        # Convertir les bateaux en tuples
        bateaux = [tuple(b) for b in donnees["bateaux"]]
        return (donnees["grille"], bateaux, donnees["nb_coules"], donnees["taille"])
    except (json.JSONDecodeError, OSError, IOError, KeyError, ValueError) as e:
        print(f"Erreur lors du chargement de la sauvegarde: {e}")
        print("Démarrage d'une nouvelle partie.")
        return None


def supprimer_sauvegarde():
    """Supprime le fichier de sauvegarde s'il existe."""
    try:
        if os.path.exists(FICHIER_SAUVEGARDE):
            os.remove(FICHIER_SAUVEGARDE)
    except OSError as e:
        print(f"Erreur lors de la suppression de la sauvegarde: {e}")


def jouer() -> None:
    """Boucle de jeu console minimaliste.

    Place des bateaux puis demande des coordonnées tant que tous les
    bateaux n'ont pas été touchés.
    """
    print("Bienvenue à la bataille navale!")

    # Vérifier s'il y a une partie sauvegardée
    partie_chargee = charger_partie()

    if partie_chargee is not None:
        reponse = input("Une partie sauvegardée a été trouvée. Voulez-vous la reprendre? (o/n): ").strip().lower()
        if reponse in ("o", "oui", "y", "yes"):
            grille, bateaux, nb_succes, taille = partie_chargee
            print(f"Partie reprise! Vous avez coulé {nb_succes}/{NB_BATEAUX} bateaux.")
        else:
            # Démarrer une nouvelle partie
            taille = demander_taille_grille()
            grille = creer_grille(taille)
            bateaux = placer_bateaux(grille, NB_BATEAUX)
            nb_succes = 0
            # Supprimer l'ancienne sauvegarde
            supprimer_sauvegarde()
    else:
        # Pas de sauvegarde, démarrer une nouvelle partie
        taille = demander_taille_grille()
        grille = creer_grille(taille)
        bateaux = placer_bateaux(grille, NB_BATEAUX)
        nb_succes = 0
    while nb_succes < NB_BATEAUX:
        print("Grille:")
        afficher_grille(grille)

        try:
            coord = demander_coordonnees(taille)
            if coord == "retry":
                if confirmation_retry_exit("Voulez-vous vraiment recommencer le jeu?"):
                    # Nettoyer la sauvegarde et relancer depuis main
                    supprimer_sauvegarde()
                    return True
                continue
            if coord == "exit":
                if confirmation_retry_exit("Voulez-vous vraiment quitter le jeu?"):
                    print("Merci d'avoir joué! Au revoir! 👋")
                    # Ne pas supprimer la sauvegarde: permettre la reprise au prochain lancement
                    return False
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
                continue  # ne pas sauvegarder si case déjà jouée

            # Sauvegarder après chaque coup valide
            sauvegarder_partie(grille, bateaux, nb_succes, taille)

        except IndexError:
            print("Coordonnées invalides. Réessayez.")

    print("\nBravo! Vous avez coulé tous les bateaux! 🎉")
    afficher_grille(grille)
    # Supprimer la sauvegarde une fois la partie terminée
    supprimer_sauvegarde()
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
