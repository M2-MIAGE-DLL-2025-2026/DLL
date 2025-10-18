"""
Tests unitaires pour la fonctionnalité de sauvegarde/reprise.
"""

import os
import json
import src.bataille_navale as bn


def setup_function():
    # Nettoyage avant chaque test
    if os.path.exists(bn.FICHIER_SAUVEGARDE):
        os.remove(bn.FICHIER_SAUVEGARDE)


def teardown_function():
    # Nettoyage après chaque test
    if os.path.exists(bn.FICHIER_SAUVEGARDE):
        os.remove(bn.FICHIER_SAUVEGARDE)


def test_sauvegarde_cree_fichier():
    grille = bn.creer_grille(5)
    bateaux = [(0, 0), (1, 1), (2, 2)]
    bn.sauvegarder_partie(grille, bateaux, nb_coules=1, taille=5)
    assert os.path.exists(bn.FICHIER_SAUVEGARDE)


def test_sauvegarde_contenu_json():
    grille = bn.creer_grille(3)
    bateaux = [(0, 0)]
    bn.sauvegarder_partie(grille, bateaux, nb_coules=0, taille=3)
    with open(bn.FICHIER_SAUVEGARDE, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert set(data.keys()) == {"grille", "bateaux", "nb_coules", "taille"}
    assert data["taille"] == 3
    assert isinstance(data["grille"], list)


def test_chargement_inexistant():
    assert bn.charger_partie() is None


def test_cycle_sauvegarde_chargement():
    taille = 6
    grille = bn.creer_grille(taille)
    bateaux = bn.placer_bateaux(grille, bn.NB_BATEAUX)
    # Simuler coups
    grille[0][0] = "O"
    grille[1][1] = "X"
    nb_coules = 1

    bn.sauvegarder_partie(grille, bateaux, nb_coules, taille)
    charge = bn.charger_partie()
    assert charge is not None
    grille2, bateaux2, nb2, taille2 = charge
    assert grille2 == grille
    assert bateaux2 == [tuple(b) for b in bateaux]
    assert nb2 == nb_coules
    assert taille2 == taille


def test_chargement_corrompu():
    with open(bn.FICHIER_SAUVEGARDE, "w", encoding="utf-8") as f:
        f.write("{ invalid json }")
    assert bn.charger_partie() is None


def test_chargement_incomplet():
    with open(bn.FICHIER_SAUVEGARDE, "w", encoding="utf-8") as f:
        json.dump({"grille": [], "bateaux": []}, f)
    assert bn.charger_partie() is None


def test_supprimer_sauvegarde():
    grille = bn.creer_grille(2)
    bn.sauvegarder_partie(grille, [], 0, 2)
    assert os.path.exists(bn.FICHIER_SAUVEGARDE)
    bn.supprimer_sauvegarde()
    assert not os.path.exists(bn.FICHIER_SAUVEGARDE)
