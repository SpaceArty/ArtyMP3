import sys, os, json
import tkinter.messagebox as messagebox
import tkinter as tk
from PIL import Image, ImageTk

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

# Constantes et paramètres
VOLUME = settings.get("volume", 50)
COULEUR_BAS = settings.get("COULEUR_BAS", "#333333")
COULEUR_FOND = settings.get("COULEUR_FOND", "#222222")

BOUCLE_OFF = settings.get("BOUCLE_OFF", 0)
BOUCLE_ONCE = settings.get("BOUCLE_ONCE", 1)
BOUCLE_ALWAYS = settings.get("BOUCLE_ALWAYS", 2)

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

def afficher_aide():
    messagebox.showinfo("Aide", "Bienvenue dans le menu aide. Ce menu contient le mode d'emplois, des réponses aux questions fréquentes, des crédits et bien plus!" \
    "Si vous avez des questions, vous pouvez venir me demander sur discord (@spacearty) ou la poster sur le github (https://github.com/SpaceArty)." \
    "\n\nUTILISATION : \n- Pour charger les fichier, il suffit de cliquer sur le bouton 'dossier' et de choisir un, ou plusieurs fichiers. Note: seul les fichiers .mp3 sont " \
    "prit en compte.\n\n- Le bouton 'shuffle' permet de randomiser tout les mp3 actuellement chargé. L'algorithme utilisé est actuellement du 'vrai' random, donc il est possible " \
    "que aucun des mp3 ne change de place si vous avez de la chance!\n\n- Le bouton 'help' ouvre se menu. Et rien d'autre de très utile. Mais laissez le, il fait de son mieux." \
    "\n\n- Les boutons 'previous' et 'next' fonctionnent (la plupart du temps) et permettent de changer de mp3 a sa guise. Note: pour ceux qui savent, ces boutons déplacent " \
    "physiquement les mp3 dans la table (réference a Annick Dupont)\n\n- Le bouton 'play' / 'pause' est modifié dynamiquement grâce a de la magie noir que certains appellent " \
    "'code'... Mais au sinon il ne fait rien d'autre de spécial que mettre en pause le mp3.\n\n - Le slider en bas a droite permet de changer le volume du mp3. " \
    "Il se rapellera du volume que vous aviez mit avant donc pas besoin de le changer a chaque lancement.\n\nQUESTIONS :\n- Aucune questions actuellement. " \
    "\n\nCREDITS :\n- SpaceArty | Code\n- Destro | Graphismes\n- ChatGPT | Le goat")