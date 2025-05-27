import os, random, tkinter as tk
from tkinter import filedialog
import silent_pygame_import  # fait l'import silencieux
import pygame  # maintenant sans message
from collections import defaultdict
from mutagen.mp3 import MP3
import utils

class PlaylistManager:
    def __init__(self, lecteur, root):
        self.lecteur = lecteur
        self.playlist = []
        self.index_courant = -1
        self.liste_prochains = None
        self.root = root

    # --------------------------------------------------------------- CHARGEMENT
    def charger_fichier(self):
        chemins = filedialog.askopenfilenames(filetypes=[("Fichiers MP3", "*.mp3")])
        if chemins:
            nouveaux = [f for f in chemins if f not in self.playlist]
            self.playlist.extend(nouveaux)
            if self.index_courant == -1 and nouveaux:
                self.index_courant = 0
                self.charger_morceau(self.playlist[self.index_courant], update_playlist=True)
            self.mettre_a_jour_liste_prochains()

    def charger_morceau(self, chemin, update_playlist=True):
        try:
            self.lecteur.fichier_en_cours = chemin
            self.lecteur.label_fichier.config(text=os.path.basename(chemin))
            pygame.mixer.music.load(chemin)

            audio = MP3(chemin)
            self.lecteur.duree_morceau = audio.info.length

            self.lecteur.progression.config(to=int(self.lecteur.duree_morceau))
            self.lecteur.progression.set(0)
            self.lecteur.en_pause = False

            if self.lecteur.en_pause:
                self.lecteur.bouton_play.config(image=self.lecteur.img_play)
            else:
                self.lecteur.bouton_play.config(image=self.lecteur.img_pause)

            if self.lecteur.label_temps_total:
                self.lecteur.label_temps_total.config(text=self.lecteur.format_temps(self.lecteur.duree_morceau))
            if self.lecteur.label_temps_courant:
                self.lecteur.label_temps_courant.config(text=self.lecteur.format_temps(0))

            self.lecteur.position_actuelle = 0
            self.lecteur.position_depart_lecture = 0
            self.lecteur.temps_debut_play = pygame.time.get_ticks() / 1000

            if update_playlist:
                if chemin in self.playlist:
                    self.index_courant = self.playlist.index(chemin)
                else:
                    self.index_courant = -1
                self.mettre_a_jour_liste_prochains()
            utils.mettre_a_jour_titre_fenetre(self.root, chemin)
        except Exception as e:
            print(f"Erreur lors du chargement du morceau: {e}")

    def charger_playlist(self):
        chemins = filedialog.askopenfilenames(filetypes=[("Fichiers MP3", "*.mp3")])
        if chemins:
            self.playlist = list(dict.fromkeys(chemins))
            self.index_courant = 0
            self.charger_morceau(self.playlist[self.index_courant], update_playlist=True)
    
    def suivant(self):
        if not self.playlist or self.index_courant == -1:
            return
        
        if self.index_courant < len(self.playlist) - 1:
            morceau_courant = self.playlist.pop(self.index_courant)
            self.playlist.append(morceau_courant)

        if not self.playlist:
            self.index_courant = -1
            return

        self.index_courant = min(self.index_courant, len(self.playlist) - 1)
        self.charger_morceau(self.playlist[self.index_courant], update_playlist=True)
        pygame.mixer.music.play()
        self.lecteur.bouton_play.config(image=self.lecteur.img_pause)
        self.mettre_a_jour_liste_prochains()

    def precedent(self):
        if self.playlist:
            self.playlist = [self.playlist[-1]] + self.playlist[:-1]

            self.index_courant = 0  # toujours le début après rotation
            self.charger_morceau(self.playlist[self.index_courant], update_playlist=False)
            pygame.mixer.music.play()
            self.lecteur.bouton_play.config(image=self.lecteur.img_pause)
            self.mettre_a_jour_liste_prochains()

    # --------------------------------------------------------------- PROCHAIN
    def lier_listbox_prochains(self, listbox):
        self.liste_prochains = listbox
        self.mettre_a_jour_liste_prochains()

    def mettre_a_jour_liste_prochains(self):
        if not self.liste_prochains or not self.playlist or self.index_courant == -1:
            return
        self.liste_prochains.delete(0, tk.END)
        n = len(self.playlist)
        for i in range(self.index_courant + 1, n):
            chemin = self.playlist[i]
            nom_fichier = os.path.basename(chemin)
            artiste = utils.get_artiste(chemin) or "Inconnu"
            affichage = f"{nom_fichier} - {artiste}"
            self.liste_prochains.insert(tk.END, affichage)

    def gestion_morceau_suivant(self, callback=None):
        if not self.playlist or self.index_courant == -1:
            if callback:
                callback()
            return

        etat_boucle = getattr(self.lecteur, 'etat_boucle', 0)

        if etat_boucle == utils.BOUCLE_OFF:
            # Gestion classique : avance dans la playlist circulaire
            if self.index_courant < len(self.playlist):
                morceau_courant = self.playlist.pop(self.index_courant)
                self.playlist.append(morceau_courant)

            if not self.playlist:
                self.index_courant = -1
                if callback:
                    callback()
                return
            self.index_courant = min(self.index_courant, len(self.playlist) - 1)

        def lancer_apres_delai():
            loops = 0
            if etat_boucle == utils.BOUCLE_ONCE:
                loops = 1  # jouer 2 fois le morceau
            elif etat_boucle == utils.BOUCLE_ALWAYS:
                loops = -1  # boucle infinie

            self.charger_morceau(self.playlist[self.index_courant], update_playlist=True)
            pygame.mixer.music.play(loops=loops, start=0.0)
            self.lecteur.bouton_play.config(image=self.lecteur.img_pause)
            self.mettre_a_jour_liste_prochains()

            # Remise à zéro de la boucle "once" après lecture
            if etat_boucle == utils.BOUCLE_ONCE:
                self.lecteur.etat_boucle = utils.BOUCLE_OFF
                self.lecteur.update_bouton_boucle()

            if callback:
                callback()

        pygame.mixer.music.stop()
        if hasattr(self.lecteur, 'fenetre') and self.lecteur.fenetre:
            self.lecteur.fenetre.after(1000, lancer_apres_delai)
        else:
            lancer_apres_delai()

    # --------------------------------------------------------------- RANDOMISATION
    def melanger_prochains(self):
        if not self.playlist or self.index_courant == -1:
            return
        if utils.settings.get("SHUFFLE_ALTERNATIF", False):
            self._melanger_par_artiste()
        else:
            self._melanger_classique()

    def _melanger_classique(self):
        prefixe = self.playlist[:self.index_courant + 1]
        suffixe = self.playlist[self.index_courant + 1:]
        random.shuffle(suffixe)
        self.playlist = prefixe + suffixe
        self.mettre_a_jour_liste_prochains()

    def _melanger_par_artiste(self):
        prefixe = self.playlist[:self.index_courant + 1]
        suffixe = self.playlist[self.index_courant + 1:]

        morceaux_par_artiste = defaultdict(list)
        for chemin in suffixe:
            artiste = utils.get_artiste(chemin)
            morceaux_par_artiste[artiste].append(chemin)

        for morceaux in morceaux_par_artiste.values():
            random.shuffle(morceaux)

        artistes = list(morceaux_par_artiste.keys())
        resultat = []

        while any(morceaux_par_artiste.values()):
            random.shuffle(artistes)
            for artiste in artistes:
                if morceaux_par_artiste[artiste]:
                    resultat.append(morceaux_par_artiste[artiste].pop(0))

        self.playlist = prefixe + resultat
        self.mettre_a_jour_liste_prochains()