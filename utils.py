import os, sys
import tkinter.messagebox as messagebox
import tkinter as tk
from PIL import Image, ImageTk
from mutagen.easyid3 import EasyID3
import settingsManager

settings_manager = settingsManager.SettingsManager()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_artiste(chemin):
    try:
        tags = EasyID3(chemin)
        return tags.get("artist", ["Inconnu"])[0]
    except Exception:
        return "Inconnu"

def mettre_a_jour_titre_fenetre(root, morceau_actuel=None):
    if morceau_actuel:
        nom_simple = os.path.basename(morceau_actuel)
        nom_sans_extension = os.path.splitext(nom_simple)[0]
        root.title(nom_sans_extension)
    else:
        root.title("ArtyMP3")

class Utils:
    def __init__(self, root, settingsManager):
        self.root = root
        self.settingsManager = settingsManager

        # Charger les couleurs
        self.COULEUR_FOND = self.settingsManager.get("COULEUR_FOND", "#222222")
        self.COULEUR_BAS = self.settingsManager.get("COULEUR_BAS", "#333333")

        self.root.configure(bg=self.COULEUR_FOND)

    def charger_image(self, nom):
        chemin = resource_path(f"Images/{nom}.png")
        image = Image.open(chemin).convert("RGBA")
        image = image.resize((30, 30), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)

    def bouton_icone(self, image, commande=None):
        btn = tk.Button(
            bg=self.COULEUR_BAS, image=image, command=commande, activebackground="#222222",
            borderwidth=0, highlightthickness=0, bd=0, relief='flat'
        )
        btn.image = image
        return btn

    def ouvrir_settings(self, img_help, img_boucle):
        self.settingsManager.settings = self.settingsManager.load_settings()

        fenetre_settings = tk.Toplevel()
        fenetre_settings.title("Paramètres")
        fenetre_settings.configure(bg=self.settingsManager.get("COULEUR_FOND", "#222222"))
        fenetre_settings.geometry("320x280")

        frame_titre = tk.Frame(fenetre_settings, bg=self.COULEUR_FOND)
        frame_titre.pack(fill=tk.X, pady=10, padx=10)

        btn_help_settings = tk.Button(frame_titre, image=img_help, command=self.afficher_aide,
                                      bg=self.COULEUR_FOND, activebackground=self.COULEUR_FOND,
                                      borderwidth=0, highlightthickness=0, relief="flat")
        btn_help_settings.pack(side=tk.LEFT)

        frame_centre = tk.Frame(frame_titre, bg=self.COULEUR_FOND)
        frame_centre.pack(side=tk.LEFT, fill=tk.X, expand=True)

        label_titre = tk.Label(frame_centre, text="Paramètres", font=("Arial", 14, "bold"),
                               bg=self.COULEUR_FOND, fg="white")
        label_titre.pack(anchor="center")

        def reset_champs():
            def_couleur_fond = self.settingsManager.get("DEFAULT_COULEUR_FOND", "#222222")
            def_couleur_bas = self.settingsManager.get("DEFAULT_COULEUR_BAS", "#333333")
            def_shuffle_alt = self.settingsManager.get("DEFAULT_SHUFFLE_ALTERNATIF", False)
            def_fenetre_dyn = self.settingsManager.get("DEFAULT_FENETRE_DYNAMIQUE", False)

            # Mise à jour UI
            entry_fond.delete(0, tk.END)
            entry_fond.insert(0, def_couleur_fond)
            entry_bas.delete(0, tk.END)
            entry_bas.insert(0, def_couleur_bas)
            var_shuffle_alt.set(def_shuffle_alt)
            var_nom_fenetre_dynamique.set(def_fenetre_dyn)

            # Mise à jour settings_manager (si tu veux vraiment écraser les defaults)
            self.settingsManager.set("DEFAULT_COULEUR_FOND", def_couleur_fond)
            self.settingsManager.set("DEFAULT_COULEUR_BAS", def_couleur_bas)
            self.settingsManager.set("DEFAULT_SHUFFLE_ALTERNATIF", def_shuffle_alt)
            self.settingsManager.set("DEFAULT_FENETRE_DYNAMIQUE", def_fenetre_dyn)


        btn_reset = tk.Button(frame_titre, image=img_boucle, command=reset_champs,
                              bg=self.COULEUR_FOND, activebackground=self.COULEUR_FOND,
                              borderwidth=0, highlightthickness=0, relief="flat")
        btn_reset.pack(side=tk.RIGHT)

        frame_couleurs = tk.Frame(fenetre_settings, bg=self.COULEUR_FOND)
        frame_couleurs.pack(pady=20, padx=20, fill=tk.X)
        frame_couleurs.grid_columnconfigure(0, weight=1)
        frame_couleurs.grid_columnconfigure(5, weight=1)

        label_fond = tk.Label(frame_couleurs, text="Couleur Fond :", bg=self.COULEUR_FOND, fg="white")
        label_fond.grid(row=0, column=0, sticky="w", padx=(0, 5))
        entry_fond = tk.Entry(frame_couleurs, width=20)
        entry_fond.grid(row=1, column=0, sticky="w", padx=(0, 15))
        entry_fond.insert(0, self.settingsManager.get("COULEUR_FOND", "#222222"))

        label_bas = tk.Label(frame_couleurs, text="Couleur Bas :", bg=self.COULEUR_FOND, fg="white")
        label_bas.grid(row=0, column=1, sticky="w", padx=(15, 5))
        entry_bas = tk.Entry(frame_couleurs, width=20)
        entry_bas.grid(row=1, column=1, sticky="w")
        entry_bas.insert(0, self.settingsManager.get("COULEUR_BAS", "#333333"))

        var_shuffle_alt = tk.BooleanVar(value=self.settingsManager.get("SHUFFLE_ALTERNATIF", False))
        check_shuffle_alt = tk.Checkbutton(fenetre_settings, text="Activer le shuffle alternatif",
                                           variable=var_shuffle_alt, onvalue=True, offvalue=False,
                                           bg=self.COULEUR_FOND, fg="white", selectcolor=self.COULEUR_FOND,
                                           activebackground=self.COULEUR_FOND)
        check_shuffle_alt.pack(pady=(10, 5))

        var_nom_fenetre_dynamique = tk.BooleanVar(value=self.settingsManager.get("FENETRE_DYNAMIQUE", False))
        check_nom_fenetre_dynamique = tk.Checkbutton(fenetre_settings, text="Activer nom de fenêtre dynamique",
                                                     variable=var_nom_fenetre_dynamique, onvalue=True, offvalue=False,
                                                     bg=self.COULEUR_FOND, fg="white", selectcolor=self.COULEUR_FOND,
                                                     activebackground=self.COULEUR_FOND)
        check_nom_fenetre_dynamique.pack(pady=(0, 10))

        def sauvegarder_params():
            new_fond = entry_fond.get()
            new_bas = entry_bas.get()
            new_shuffle_alt = var_shuffle_alt.get()
            new_nom_fenetre_dynamique = var_nom_fenetre_dynamique.get()

            self.settingsManager.set("COULEUR_FOND", new_fond)
            self.settingsManager.set("COULEUR_BAS", new_bas)
            self.settingsManager.set("SHUFFLE_ALTERNATIF", new_shuffle_alt)
            self.settingsManager.set("FENETRE_DYNAMIQUE", new_nom_fenetre_dynamique)

            fenetre_settings.destroy()

        btn_sauvegarder = tk.Button(fenetre_settings, text="Sauvegarder", command=sauvegarder_params,
                                    bg=self.COULEUR_BAS, fg="white", font=("Arial", 12))
        btn_sauvegarder.pack(pady=15, ipadx=10, ipady=5)

    def afficher_aide(self):
        messagebox.showinfo(
            "Aide",
            "Bienvenue dans le menu aide. Ce menu contient le mode d'emplois, des réponses aux questions fréquentes, des crédits et bien plus!"
            "Si vous avez des questions, vous pouvez venir me demander sur discord (@spacearty) ou la poster sur le GitHub : https://github.com/SpaceArty/ArtyMP3/"
            "\n\nUTILISATION : \nPour charger les fichier, il suffit de cliquer sur le bouton 'dossier' et de choisir un, ou plusieurs fichiers. Note: seul les fichiers .mp3 sont "
            "prit en compte.\n\nLe bouton 'shuffle' permet de randomiser tout les mp3 actuellement chargé. L'algorithme utilisé est actuellement du 'vrai' random, donc il est possible "
            "que aucun des mp3 ne change de place si vous avez de la chance!\n\nLe bouton 'paramètre' ouvre un sous menu. Et rien d'autre de très utile. Mais laissez le, il fait de son mieux."
            "\n\nLes boutons 'previous' et 'next' fonctionnent (la plupart du temps) et permettent de changer de mp3 a sa guise. Note: pour ceux qui savent, ces boutons déplacent "
            "physiquement les mp3 dans la table (réference a Annick Dupont)\n\nLe bouton 'play' / 'pause' est modifié dynamiquement grâce a de la magie noir que certains appellent "
            "'code'... Mais au sinon il ne fait rien d'autre de spécial que mettre en pause le mp3.\n\nLe slider en bas a droite permet de changer le volume du mp3. "
            "Il se rapellera du volume que vous aviez mit avant donc pas besoin de le changer a chaque lancement.\n\nQUESTIONS :\nQ : Que fait le 'Shuffle Alternatif' ?"
            " R : C'est une fonction en BETA qui permet de mélanger les MP3 en fonctione des artistes. Note : Les métadonnées du fichier MP3 sont nécessaire. "
            "Si a coté du titre du MP3 c'est marqué 'Inconnu', ca veut dire qu'elles sont manquantes.\n\nQ : A quoi sert le 'Nom de Fenêtre Dynamique' ? "
            "R : Ça change le nom de la fenêtre en fonction du MP3 actuel."
            "\n\nCREDITS :\nSpaceArty | Code\nDestro | Graphismes\nChatGPT | Le goat"
        )