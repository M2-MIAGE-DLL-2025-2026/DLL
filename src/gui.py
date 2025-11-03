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
    from src.bataille_navale import creer_grille, placer_bateaux


class GuiApp:  # pylint: disable=too-many-instance-attributes
    """
    Interface graphique minimale pour la bataille navale.

    Ce prototype utilise Tkinter et réutilise les fonctions de logique
    présentes dans `bataille_navale.py`. L'objectif est d'avoir une fenêtre
    avec une grille de boutons cliquables, un label de statut et quelques
    contrôles simples (nouvelle partie, compteur de tirs/touches).
    """

    def __init__(self, master, size=5, boats=3):
        self.master = master
        self.size = size
        self.boats = boats
        master.title("Bataille Navale - GUI (prototype)")

        # Frame principale qui contiendra la grille
        self.frame = tk.Frame(master)
        self.frame.pack()

        # Label de statut
        self.status = tk.StringVar()
        self.status.set("Prêt")
        self.status_label = tk.Label(master, textvariable=self.status)
        self.status_label.pack(pady=5)

        # Compteurs de tirs et de touches
        self.tirs = 0
        self.touches = 0
        self.compteur = tk.StringVar()
        self.compteur.set(f"Tirs : {self.tirs} | Touches : {self.touches}")
        self.compteur_label = tk.Label(master, textvariable=self.compteur)
        self.compteur_label.pack(pady=5)

        # Liste 2D de boutons (widgets) et grille logique
        self.buttons = []
        self.grille = creer_grille(self.size)
        placer_bateaux(self.grille, self.boats)

        for i in range(self.size):
            row = []
            for j in range(self.size):
                b = tk.Button(
                    self.frame, text="~", width=3, height=1,
                    command=lambda x=i, y=j: self.on_click(x, y)
                )
                b.grid(row=i, column=j)
                row.append(b)
            self.buttons.append(row)

        # Frame pour les contrôles
        self.controls = tk.Frame(master)
        self.controls.pack()

        # Bouton Nouvelle Partie
        self.new_button = tk.Button(
            self.controls, text="Nouvelle partie", command=self.new_game
        )
        self.new_button.pack(side=tk.LEFT, padx=5)

    def on_click(self, x, y):
        """Gérer un clic utilisateur sur la case (x, y)."""
        val = self.grille[x][y]
        if val == 'B':
            self.buttons[x][y].config(text='X', bg='red')
            self.grille[x][y] = 'X'
            self.status.set('Touché !')
            self.tirs += 1
            self.touches += 1
        elif val == '~':
            self.buttons[x][y].config(text='O', bg='light blue')
            self.grille[x][y] = 'O'
            self.status.set('Raté')
            self.tirs += 1
        else:
            self.status.set('Case déjà jouée')
            return  # Ne compte pas les tirs déjà joués

        # Mettre à jour l'affichage du compteur
        self.compteur.set(f"Tirs : {self.tirs} | Touches : {self.touches}")

    def new_game(self):
        """Réinitialiser la grille et les compteurs pour une nouvelle partie."""
        self.grille = creer_grille(self.size)
        placer_bateaux(self.grille, self.boats)

        for i in range(self.size):
            for j in range(self.size):
                self.buttons[i][j].config(text='~', bg='SystemButtonFace')

        # Réinitialiser statut et compteurs
        self.status.set('Nouvelle partie')
        self.tirs = 0
        self.touches = 0
        self.compteur.set(f"Tirs : {self.tirs} | Touches : {self.touches}")


def run_gui(size=5, boats=3):
    """Lance l'interface graphique."""
    root = tk.Tk()
    gui_app = GuiApp(root, size=size, boats=boats)
    _ = gui_app  # garder référence
    root.mainloop()


def main():
    """Point d'entrée pour exécution en tant que script."""
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
