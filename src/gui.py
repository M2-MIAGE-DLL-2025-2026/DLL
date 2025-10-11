"""Interface graphique minimale (Tkinter) pour le projet Bataille Navale.

Ce module fournit un prototype d'interface graphique réutilisant la
logique définie dans `bataille_navale.py`. Il est volontairement simple
et sert de point de départ pour améliorer l'UX.
"""

import tkinter as tk
import sys

# Importer la logique du jeu depuis le module existant

try:
    from bataille_navale import creer_grille, placer_bateaux
except ImportError:
    # si le chemin de module est différent (p.ex. exécution depuis racine),
    # on tente l'import via le package src
    from src.bataille_navale import creer_grille, placer_bateaux


class GuiApp:  # pylint: disable=too-many-instance-attributes
    """
    Interface graphique minimale pour la bataille navale.

    Ce prototype utilise Tkinter et réutilise les fonctions de logique
    présentes dans `bataille_navale.py`. L'objectif est d'avoir une fenêtre
    avec une grille de boutons cliquables, un label de statut et quelques
    contrôles simples (nouvelle partie, révéler pour debug).
    """

    def __init__(self, master, size=5, boats=3, vies=5):
        # maître Tk et paramètres de jeu
        self.master = master
        self.size = size
        self.boats = boats
        self.vies = vies
        master.title("Bataille Navale - GUI (prototype)")

        # Frame principale qui contiendra la grille
        self.frame = tk.Frame(master)
        self.frame.pack()

        # Variable de statut affichée en haut/bas de la fenêtre
        self.status = tk.StringVar()
        self.status.set("Prêt")

    # Liste 2D de boutons (widgets) et initialisation de la grille logique
        self.buttons = []
        self.grille = creer_grille(self.size)  # crée une matrice size x size
        placer_bateaux(self.grille, self.boats)  # place aléatoirement les bateaux

    # Création des boutons pour chaque case.
        for i in range(self.size):
            row = []
            for j in range(self.size):
                b = tk.Button(self.frame, text="~", width=3, height=1,
                              command=lambda x=i, y=j: self.on_click(x, y))
                b.grid(row=i, column=j)
                row.append(b)
            self.buttons.append(row)

        # Label qui affiche un message d'état (touché/râté/etc.)
        self.status_label = tk.Label(master, textvariable=self.status)
        self.status_label.pack(pady=5)

        # Frame pour les contrôles (boutons)
        self.controls = tk.Frame(master)
        self.controls.pack()

        # Bouton pour démarrer une nouvelle partie (réinitialise la grille)
        self.new_button = tk.Button(self.controls, text="Nouvelle partie", command=self.new_game)
        self.new_button.pack(side=tk.LEFT, padx=5)


    def on_click(self, x, y):
        """Gérer un clic utilisateur sur la case (x, y).

        Met à jour la représentation visuelle et l'état logique de la grille
        selon le contenu de la case (bateau, eau ou déjà joué).
        """
        val = self.grille[x][y]
        if val == 'B':
            # Bateau touché → marquer 'X' en rouge
            self.buttons[x][y].config(text='X', bg='red')
            self.grille[x][y] = 'X'
            self.status.set(f'Touché !')
        elif val == '~':
            # Eau → marquer 'O' en bleu clair
            self.buttons[x][y].config(text='O', bg='light blue')
            self.grille[x][y] = 'O'
            self.vies -= 1
            if self.vies > 0:
                self.status.set(f'Raté, il vous reste {self.vies} vies.')
            else:
                self.status.set('Rate! Il ne vous reste plus aucune vie, vous avez perdu.')
        else:
            # Case déjà jouée (X ou O)
            self.status.set('Case déjà jouée')

    def new_game(self):
        """Réinitialiser la grille logique et l'interface pour une nouvelle partie."""
        self.grille = creer_grille(self.size)
        placer_bateaux(self.grille, self.boats)
        self.vies = 50
        for i in range(self.size):
            for j in range(self.size):
                # Remet le texte du bouton à '~' et la couleur par défaut
                self.buttons[i][j].config(text='~', bg='SystemButtonFace')
        self.status.set('Nouvelle partie')



def run_gui(size=5, boats=3):
    """Lance l'interface graphique avec les paramètres donnés.

    Args:
        size: taille de la grille (par défaut 5).
        boats: nombre de bateaux (par défaut 3).
    """
    root = tk.Tk()
    gui_app = GuiApp(root, size=size, boats=boats)
    # garder une référence explicite à l'application pour éviter l'avertissement
    # pylint: disable=unused-variable
    _ = gui_app
    root.mainloop()


def main():
    """Point d'entrée pour exécution en tant que script.

    Lit deux arguments positionnels optionnels : size et boats.
    """
    size_val = 5
    boats_val = 3
    if len(sys.argv) >= 2:
        try:
            size_val = int(sys.argv[1])
        except ValueError:
            pass
    if len(sys.argv) >= 3:
        try:
            boats_val = int(sys.argv[2])
        except ValueError:
            pass
    run_gui(size=size_val, boats=boats_val)


if __name__ == '__main__':
    main()
