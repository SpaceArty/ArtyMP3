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
            "Bienvenue dans le menu aide. Ce menu est un tutoriel bref de comment utiliser cette app. Pour plus d'informations, allez lire le README sur la page github. " \
            "https://github.com/SpaceArty/ArtyMP3\n\nComment charger des fichiers ?\nCliquer sur le bouton dossier, ca ouvrira l'explorateur de fichiers. Ensuite il faut choisir" \
            "quelles mp3 vous voulez lire. Pour tester si tout fonctionne, lors du téléchargement il y a eut un dossier appelé SELECT ME TO TEST. Choisisez ce dossier, il y a quelque" \
            "mp3 dedans. Sélectionez les tous (CTRL-A) puis confirmez le choix (ENTER). Et voila, tout fonctionne désormais, vous avez votre liste de mp3.\n\nMaintenant vous pouvez" \
            "créer un dossier avec vos propres mp3 et le sélectioner pour tous les lire."
        )