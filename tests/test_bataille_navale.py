"""Tests unitaires d'initialisation du jeu de Bataille Navale."""
import io
from contextlib import redirect_stdout
import src.bataille_navale as bn

def test_creer_grille_dimensions():
    """
    La grille doit avoir la bonne taille N x N.
    """
    for size in (1, 3, 5):
        g = bn.creer_grille(size)
        assert isinstance(g, list)
        assert len(g) == size
        assert all(isinstance(row, list) for row in g)
        assert all(len(row) == size for row in g)

def test_creer_grille_contenu_par_defaut():
    """
    Toutes les cases sont initialisées à '~'.
    """
    size = 4
    g = bn.creer_grille(size)
    assert all(cell == "~" for row in g for cell in row)

def test_creer_grille_lignes_independantes():
    """
    Chaque ligne est indépendante (pas d'aliasing entre lignes).
    """
    size = 3
    g = bn.creer_grille(size)
    g[0][0] = "X"
    assert g[1][0] == "~" and g[2][0] == "~"

def test_creer_grille_size_zero():
    """
    Comportement simple attendu pour size=0 : grille vide.
    """
    assert bn.creer_grille(0) == []

def test_afficher_grille_simple():
    """
    afficher_grille doit imprimer une grille simple.
    """
    grille = [
        ["~", "~"],
        ["~", "~"],
    ]
    buf = io.StringIO()
    with redirect_stdout(buf):
        bn.afficher_grille(grille)
    out = buf.getvalue().strip()
    lignes = out.splitlines()
    assert len([l for l in lignes if l.strip()]) == 2
    assert all("~" in l for l in lignes)

def test_afficher_grille_masque_bateaux():
    """
    Les 'B' doivent être masqués en '~' lors de l'affichage.
    """
    grille = [
        ["~", "B", "~"],
        ["B", "~", "~"],
    ]
    buf = io.StringIO()
    with redirect_stdout(buf):
        bn.afficher_grille(grille)
    out = buf.getvalue()
    assert "B" not in out
    assert "~" in out

def test_afficher_grille_vide():
    """
    Une grille vide ne doit pas planter et ne rien afficher d'utile.
    """
    grille = []
    buf = io.StringIO()
    with redirect_stdout(buf):
        bn.afficher_grille(grille)
    out = buf.getvalue().strip()
    assert out == ""

def test_afficher_grille_avec_symboles_partie():
    """
    Les symboles ('X', 'O') doivent être affichés tels quels, mais B caché.
    """
    grille = [
        ["X", "O"],
        ["~", "B"],
    ]
    buf = io.StringIO()
    with redirect_stdout(buf):
        bn.afficher_grille(grille)
    out = buf.getvalue()
    assert "X" in out
    assert "O" in out
    assert "B" not in out
