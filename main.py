import tkinter as tk, utils
from PIL import Image, ImageTk
from lecteurMP3 import LecteurMP3
from playlist import PlaylistManager
from slider import SliderCustom

COULEUR_FOND = utils.COULEUR_FOND
COULEUR_BAS = utils.COULEUR_BAS
bouton_icone = utils.bouton_icone
ouvrir_settings = utils.ouvrir_settings
charger_image = utils.charger_image

# pyinstaller --onefile --windowed --add-data "settings.json;." --add-data "Images;Images" --name ArtyMP3 main.py
# La commande ci dessus permet de créer le fichier .exe une fois des changements effectués.

fenetre = tk.Tk()
fenetre.title("ArtyMP3")
fenetre.geometry("700x350")
fenetre.configure(bg=COULEUR_FOND)
style_label = {"bg": COULEUR_FOND, "fg": "white", "font": ("Arial", 10)}

img_play = charger_image("play")
img_pause = charger_image("pause")
img_load = charger_image("dossier")
img_prev = charger_image("previous")
img_next = charger_image("next")
img_random = charger_image("random")
img_help = charger_image("help")
img_boucle = charger_image("loop")
img_boucle_once = charger_image("loop1")
img_boucle_always = charger_image("loop2")
img_settings = charger_image("settings")

frame_global = tk.Frame(fenetre, bg=COULEUR_FOND)
frame_global.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

frame_progression = tk.Frame(frame_global, bg=COULEUR_FOND)  # --------------------------------------------------------------- BARRE DE PROGRESSION + TEMPS + AIDE
frame_progression.pack(fill=tk.X, pady=(0, 10))

btn_settings = tk.Button(frame_progression, image=img_settings, command=lambda: ouvrir_settings(img_help, img_boucle), bg=COULEUR_FOND,
    activebackground=COULEUR_FOND, borderwidth=0, highlightthickness=0, relief="flat")
btn_settings.grid(in_=frame_progression, row=0, column=0, padx=(5, 5))

label_temps_courant = tk.Label(frame_progression, text="00:00", **style_label)
label_temps_courant.grid(row=0, column=1, padx=(5, 5))

progression = tk.Scale(frame_progression, from_=0, to=100, orient=tk.HORIZONTAL,
                       bg=COULEUR_FOND, fg="white", troughcolor="#444444",
                       highlightthickness=0, showvalue=False)
progression.grid(row=0, column=2, sticky="ew", pady=5)

label_temps_total = tk.Label(frame_progression, text="00:00", **style_label)
label_temps_total.grid(row=0, column=3, padx=(5, 10))

frame_progression.columnconfigure(2, weight=1)

label_prochains = tk.Label(frame_global, text="À venir :", **style_label)  # --------------------------------------------------------------- LISTE PROCHAINS
label_prochains.pack(anchor="w")

frame_liste_prochains = tk.Frame(frame_global, bg=COULEUR_FOND)
frame_liste_prochains.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

liste_prochains = tk.Listbox(frame_liste_prochains, height=10, bg=COULEUR_FOND,
                             fg="white", selectbackground="#333333",
                             selectforeground="white", highlightthickness=0)
liste_prochains.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar_prochains = tk.Scrollbar(frame_liste_prochains, orient=tk.VERTICAL, command=liste_prochains.yview)
scrollbar_prochains.pack(side=tk.RIGHT, fill=tk.Y)

liste_prochains.config(yscrollcommand=scrollbar_prochains.set)

label_fichier = tk.Label(frame_global, text="Aucun fichier sélectionné", **style_label)
label_fichier.pack(pady=(0, 10))

frame_bas = tk.Frame(fenetre, bg=COULEUR_BAS)  # --------------------------------------------------------------- FRAME EN BAS
frame_bas.pack(side=tk.BOTTOM, fill=tk.X)

frame_charger_random = tk.Frame(frame_bas, bg=COULEUR_BAS)
frame_charger_random.pack(side=tk.LEFT, pady=10, padx=10)

frame_controls = tk.Frame(frame_bas, bg=COULEUR_BAS)
frame_controls.pack(side=tk.LEFT, expand=True)

frame_volume = tk.Frame(frame_bas, bg=COULEUR_BAS)   # --------------------------------------------------------------- VOLUME
frame_volume.pack(side=tk.RIGHT, padx=20)

label_volume = tk.Label(frame_volume, text="Volume", bg=COULEUR_BAS, fg="white", font=("Arial", 10))
label_volume.grid(row=0, column=0, sticky="w")

label_valeur_volume = tk.Label(frame_volume, text="100", bg=COULEUR_BAS, fg="white", font=("Arial", 10))
label_valeur_volume.grid(row=0, column=1, sticky="e", padx=(0, 0))

slider_volume = SliderCustom(frame_volume, length=100)
slider_volume.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(2, 0))

frame_volume.columnconfigure(0, weight=1)
frame_volume.columnconfigure(1, weight=0)

lecteur = LecteurMP3(label_fichier, progression, None, img_play, img_pause, slider_volume, fenetre)  # --------------------------------------------------------------- LECTEUR
gestion_playlist = PlaylistManager(lecteur, fenetre)
gestion_playlist.lier_listbox_prochains(liste_prochains)
lecteur.playlist_manager = gestion_playlist
slider_volume.set_callback(lecteur.changer_volume)
lecteur.label_valeur_volume = label_valeur_volume
label_valeur_volume.config(text=str(lecteur.volume))

btn_charger = bouton_icone(img_load, gestion_playlist.charger_fichier)  # --------------------------------------------------------------- BOUTON GAUCHE (charger, random, loop)
btn_charger.pack(in_=frame_charger_random, side=tk.LEFT, padx=(0, 5))

btn_random = bouton_icone(img_random, lambda: gestion_playlist.melanger_prochains())
btn_random.pack(in_=frame_charger_random, side=tk.LEFT, padx=(5, 0))

btn_boucle = bouton_icone(img_boucle, lambda: lecteur.toggle_boucle())
btn_boucle.pack(in_=frame_charger_random, side=tk.LEFT, padx=(5, 5))
lecteur.btn_boucle = btn_boucle
lecteur.img_boucle = img_boucle
lecteur.img_boucle_once = img_boucle_once
lecteur.img_boucle_always = img_boucle_always
lecteur.update_bouton_boucle()

btn_prev = bouton_icone(img_prev, gestion_playlist.precedent)  # --------------------------------------------------------------- BOUTONS EN BAS (précédent, pause, suivant)
btn_prev.pack(in_=frame_controls, side=tk.LEFT, padx=10, pady=10)

bouton_play = bouton_icone(img_play, lambda: lecteur.jouer_ou_pause(img_play, img_pause))
bouton_play.pack(in_=frame_controls, side=tk.LEFT, padx=10, pady=10)
lecteur.bouton_play = bouton_play

btn_next = bouton_icone(img_next, gestion_playlist.suivant)
btn_next.pack(in_=frame_controls, side=tk.LEFT, padx=10, pady=10)

progression.bind("<ButtonPress-1>", lecteur.debut_seek)  # --------------------------------------------------------------- LES BOUTONS
progression.bind("<ButtonRelease-1>", lambda e: lecteur.fin_seek(progression, e))
progression.bind("<B1-Motion>", lambda e: lecteur.mettre_a_jour_temps_courant(label_temps_courant))
fenetre.bind("<space>", lambda e: lecteur.jouer_ou_pause(img_play, img_pause))

lecteur.lier_labels_temps(fenetre, label_temps_courant, label_temps_total)  # --------------------------------------------------------------- BELLO BOUCLO
fenetre.mainloop()