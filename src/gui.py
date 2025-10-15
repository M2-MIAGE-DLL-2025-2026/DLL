"""Interface graphique minimale (Tkinter) pour le projet Bataille Navale.

Ce module fournit un prototype d'interface graphique réutilisant la
logique définie dans `bataille_navale.py`. Il est volontairement simple
et sert de point de départ pour améliorer l'UX.
"""

import tkinter as tk
from tkinter import messagebox
import sys

# Importer la logique du jeu depuis le module existant

try:
    from bataille_navale import (
        creer_grille,
        placer_bateaux,
        sauvegarder_partie,
        charger_partie,
        supprimer_sauvegarde,
        NB_BATEAUX,
    )
except ImportError:
    # si le chemin de module est différent (p.ex. exécution depuis racine),
    # on tente l'import via le package src
    from src.bataille_navale import (
        creer_grille,
        placer_bateaux,
        sauvegarder_partie,
        charger_partie,
        supprimer_sauvegarde,
        NB_BATEAUX,
    )


class GuiApp:  # pylint: disable=too-many-instance-attributes
    """
    Interface graphique minimale pour la bataille navale.

    Ce prototype utilise Tkinter et réutilise les fonctions de logique
    présentes dans `bataille_navale.py`. L'objectif est d'avoir une fenêtre
    avec une grille de boutons cliquables, un label de statut et quelques
    contrôles simples (nouvelle partie, révéler pour debug).
    """

    def __init__(self, master, size=5, boats=3):
        # maître Tk et paramètres de jeu
        self.master = master
        self.size = size
        self.boats = boats
        master.title("Bataille Navale - GUI (prototype)")

        # Frame principale qui contiendra la grille
        self.frame = tk.Frame(master)
        self.frame.pack()

        # Variable de statut affichée en haut/bas de la fenêtre
        self.status = tk.StringVar()
        self.status.set("Prêt")

        # Etat logique
        self.grille = None
        self.buttons = []
        self.bateaux = []
        self.nb_coules = 0

        # Reprise de partie si disponible
        partie = charger_partie()
        if partie is not None and messagebox.askyesno(
            "Reprendre la partie",
            "Une partie sauvegardée a été trouvée. Voulez-vous la reprendre?",
        ):
            grille_s, bateaux_s, nb_coules_s, taille_s = partie
            # Ajuster la taille de la GUI à la sauvegarde
            self.size = taille_s
            self.grille = grille_s
            self.bateaux = bateaux_s
            self.nb_coules = nb_coules_s
        else:
            # Nouvelle partie
            self.grille = creer_grille(self.size)
            self.bateaux = placer_bateaux(self.grille, self.boats)
            self.nb_coules = 0
            # Si l'utilisateur a refusé la reprise, nettoyer l'ancienne sauvegarde
            supprimer_sauvegarde()

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

        # Mettre l'interface en cohérence avec l'état courant
        self.mettre_a_jour_interface()


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
            self.nb_coules += 1
            self.status.set(f"Touché ! ({self.nb_coules}/{self.boats})")
            # Sauvegarde
            sauvegarder_partie(self.grille, self.bateaux, self.nb_coules, self.size)
            # Victoire ?
            if self.nb_coules >= self.boats:
                messagebox.showinfo("Victoire", "Bravo! Vous avez coulé tous les bateaux!")
                supprimer_sauvegarde()
        elif val == '~':
            # Eau → marquer 'O' en bleu clair
            self.buttons[x][y].config(text='O', bg='light blue')
            self.grille[x][y] = 'O'
            self.status.set('Raté')
            # Sauvegarde
            sauvegarder_partie(self.grille, self.bateaux, self.nb_coules, self.size)
        else:
            # Case déjà jouée (X ou O)
            self.status.set('Case déjà jouée')

    def new_game(self):
        """Réinitialiser la grille logique et l'interface pour une nouvelle partie."""
        supprimer_sauvegarde()
        self.grille = creer_grille(self.size)
        self.bateaux = placer_bateaux(self.grille, self.boats)
        self.nb_coules = 0
        for i in range(self.size):
            for j in range(self.size):
                # Remet le texte du bouton à '~' et la couleur par défaut
                self.buttons[i][j].config(text='~', bg='SystemButtonFace')
        self.status.set('Nouvelle partie')

    def mettre_a_jour_interface(self):
        """Met à jour l'UI selon l'état de la grille."""
        for i in range(self.size):
            for j in range(self.size):
                val = self.grille[i][j]
                if val == 'X':
                    self.buttons[i][j].config(text='X', bg='red')
                elif val == 'O':
                    self.buttons[i][j].config(text='O', bg='light blue')
                else:
                    self.buttons[i][j].config(text='~', bg='SystemButtonFace')



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
