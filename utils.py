import sys, os, json
import tkinter.messagebox as messagebox
import tkinter as tk
from PIL import Image, ImageTk
from mutagen.easyid3 import EasyID3

# --------------------------------------------------------------- LE GOAT
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_settings():
    chemin = resource_path("settings.json")
    try:
        with open(chemin, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

settings = load_settings()
VOLUME = settings.get("volume", 50)
COULEUR_BAS = settings.get("COULEUR_BAS", "#333333")
COULEUR_FOND = settings.get("COULEUR_FOND", "#222222")

BOUCLE_OFF = settings.get("BOUCLE_OFF", 0)
BOUCLE_ONCE = settings.get("BOUCLE_ONCE", 1)
BOUCLE_ALWAYS = settings.get("BOUCLE_ALWAYS", 2)
SHUFFLE_ALTERNATIF = settings.get("SHUFFLE_ALTERNATIF", False)

# --------------------------------------------------------------- ET LE RESTE
def charger_image(nom):
    chemin = resource_path(f"Images/{nom}.png")
    image = Image.open(chemin).convert("RGBA")
    image = image.resize((30, 30), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(image)

def bouton_icone(image, commande=None):
    btn = tk.Button(
        bg=COULEUR_BAS, image=image, command=commande, activebackground="#222222",
        borderwidth=0, highlightthickness=0, bd=0, relief='flat'
    )
    btn.image = image
    return btn

def get_artiste(chemin):
    try:
        tags = EasyID3(chemin)
        return tags.get("artist", ["Inconnu"])[0]
    except Exception:
        return "Inconnu"

def ouvrir_settings(img_help, img_boucle):
    settings_actuels = load_settings()

    fenetre_settings = tk.Toplevel()
    fenetre_settings.title("Paramètres")
    fenetre_settings.configure(bg=settings_actuels.get("COULEUR_FOND", "#222222"))
    fenetre_settings.geometry("320x250")

    frame_titre = tk.Frame(fenetre_settings, bg=COULEUR_FOND)
    frame_titre.pack(fill=tk.X, pady=10, padx=10)

    btn_help_settings = tk.Button(frame_titre, image=img_help, command=afficher_aide,
                                  bg=COULEUR_FOND, activebackground=COULEUR_FOND,
                                  borderwidth=0, highlightthickness=0, relief="flat")
    btn_help_settings.pack(side=tk.LEFT)

    # Frame intermédiaire pour centrer le label
    frame_centre = tk.Frame(frame_titre, bg=COULEUR_FOND)
    frame_centre.pack(side=tk.LEFT, fill=tk.X, expand=True)

    label_titre = tk.Label(frame_centre, text="Paramètres", font=("Arial", 14, "bold"),
                           bg=COULEUR_FOND, fg="white")
    label_titre.pack(anchor="center")  # centrer horizontalement dans ce frame

    # Définir reset_champs AVANT d'utiliser btn_reset
    def reset_champs():
        entry_fond.delete(0, tk.END)
        entry_fond.insert(0, settings.get("DEFAULT_COULEUR_FOND", "#222222"))
        entry_bas.delete(0, tk.END)
        entry_bas.insert(0, settings.get("DEFAULT_COULEUR_BAS", "#333333"))
        var_shuffle_alt.set(settings.get("DEFAULT_SHUFFLE_ALTERNATIF", False))

    btn_reset = tk.Button(frame_titre, image=img_boucle, command=reset_champs,
                          bg=COULEUR_FOND, activebackground=COULEUR_FOND,
                          borderwidth=0, highlightthickness=0, relief="flat")
    btn_reset.pack(side=tk.RIGHT)

    frame_couleurs = tk.Frame(fenetre_settings, bg=COULEUR_FOND)
    frame_couleurs.pack(pady=20, padx=20, fill=tk.X)
    frame_couleurs.grid_columnconfigure(0, weight=1)
    frame_couleurs.grid_columnconfigure(5, weight=1)

    # Champ couleur fond
    label_fond = tk.Label(frame_couleurs, text="Couleur Fond :", bg=COULEUR_FOND, fg="white")
    label_fond.grid(row=0, column=0, sticky="w", padx=(0,5))
    entry_fond = tk.Entry(frame_couleurs, width=20)
    entry_fond.grid(row=1, column=0, sticky="w", padx=(0,15))
    entry_fond.insert(0, settings.get("COULEUR_FOND", "#222222"))

    # Champ couleur bas
    label_bas = tk.Label(frame_couleurs, text="Couleur Bas :", bg=COULEUR_FOND, fg="white")
    label_bas.grid(row=0, column=1, sticky="w", padx=(15,5))
    entry_bas = tk.Entry(frame_couleurs, width=20)
    entry_bas.grid(row=1, column=1, sticky="w", padx=(0,0))
    entry_bas.insert(0, settings.get("COULEUR_BAS", "#333333"))

    # Champ Shuffle alternatif
    var_shuffle_alt = tk.BooleanVar(value=settings_actuels.get("SHUFFLE_ALTERNATIF", False))
    check_shuffle_alt = tk.Checkbutton(fenetre_settings, text="Activer le shuffle alternatif",
                                       variable=var_shuffle_alt, onvalue=True, offvalue=False,
                                       bg=COULEUR_FOND, fg="white", selectcolor=COULEUR_FOND,
                                       activebackground=COULEUR_FOND)
    check_shuffle_alt.pack(pady=(10, 5))

    def sauvegarder_params():
        new_fond = entry_fond.get()
        new_bas = entry_bas.get()
        new_shuffle_alt = var_shuffle_alt.get()

        print(f"Nouvelle couleur fond : {new_fond}")
        print(f"Nouvelle couleur bas : {new_bas}")
        print(f"Shuffle alternatif : {new_shuffle_alt}")

        # Sauvegarder les paramètres
        new_settings = settings_actuels.copy()
        new_settings["COULEUR_FOND"] = new_fond
        new_settings["COULEUR_BAS"] = new_bas
        new_settings["SHUFFLE_ALTERNATIF"] = new_shuffle_alt

        chemin = resource_path("settings.json")
        try:
            with open(chemin, "w", encoding="utf-8") as f:
                json.dump(new_settings, f, indent=4)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")
        global settings
        settings = load_settings()
        fenetre_settings.destroy()

    btn_sauvegarder = tk.Button(fenetre_settings, text="Sauvegarder", command=sauvegarder_params,
                                bg=COULEUR_BAS, fg="white", font=("Arial", 12))
    btn_sauvegarder.pack(pady=15, ipadx=10, ipady=5)

    fenetre_settings.mainloop()

def afficher_aide():
    messagebox.showinfo("Aide", "Bienvenue dans le menu aide. Ce menu contient le mode d'emplois, des réponses aux questions fréquentes, des crédits et bien plus!" \
    "Si vous avez des questions, vous pouvez venir me demander sur discord (@spacearty) ou la poster sur le github (https://github.com/SpaceArty/ArtyMP3/)." \
    "\n\nUTILISATION : \nPour charger les fichier, il suffit de cliquer sur le bouton 'dossier' et de choisir un, ou plusieurs fichiers. Note: seul les fichiers .mp3 sont " \
    "prit en compte.\n\nLe bouton 'shuffle' permet de randomiser tout les mp3 actuellement chargé. L'algorithme utilisé est actuellement du 'vrai' random, donc il est possible " \
    "que aucun des mp3 ne change de place si vous avez de la chance!\n\nLe bouton 'paramètre' ouvre un sous menu. Et rien d'autre de très utile. Mais laissez le, il fait de son mieux." \
    "\n\nLes boutons 'previous' et 'next' fonctionnent (la plupart du temps) et permettent de changer de mp3 a sa guise. Note: pour ceux qui savent, ces boutons déplacent " \
    "physiquement les mp3 dans la table (réference a Annick Dupont)\n\nLe bouton 'play' / 'pause' est modifié dynamiquement grâce a de la magie noir que certains appellent " \
    "'code'... Mais au sinon il ne fait rien d'autre de spécial que mettre en pause le mp3.\n\nLe slider en bas a droite permet de changer le volume du mp3. " \
    "Il se rapellera du volume que vous aviez mit avant donc pas besoin de le changer a chaque lancement.\n\nQUESTIONS :\nAucune questions actuellement. " \
    "\n\nCREDITS :\nSpaceArty | Code\nDestro | Graphismes\nChatGPT | Le goat")