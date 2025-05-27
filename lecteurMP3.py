import silent_pygame_import
import pygame, json
from playlist import PlaylistManager

SETTINGS_FILE = "settings.json"
BOUCLE_OFF, BOUCLE_ONCE, BOUCLE_ALWAYS = 0, 1, 2

class LecteurMP3:
    def __init__(self, label_fichier, progression, bouton_play, img_play=None, img_pause=None, slider_volume=None,
                 btn_boucle=None, img_boucle=None, img_boucle_once=None, img_boucle_always=None, root=None):
        pygame.init()
        pygame.mixer.init()

        # Références widgets UI
        self.label_fichier = label_fichier
        self.progression = progression
        self.bouton_play = bouton_play
        self.img_play = img_play
        self.img_pause = img_pause
        self.slider_volume = slider_volume

        # Nouveaux éléments pour le bouton boucle
        self.etat_boucle = BOUCLE_OFF
        self.btn_boucle = btn_boucle
        self.img_boucle = img_boucle
        self.img_boucle_once = img_boucle_once
        self.img_boucle_always = img_boucle_always

        # Variables pour la lecture
        self.position_depart_lecture = 0
        self.seek_en_cours_manuel = False
        self.etat_avant_seek = False
        self.en_pause_temp = False
        self.position_actuelle = 0
        self.temps_debut_play = 0
        self.en_pause = False
        self.fichier_en_cours = None
        self.duree_morceau = 0
        self.changement_en_cours = False

        # Labels temps à lier plus tard
        self.label_temps_courant = None
        self.label_temps_total = None
        self.fenetre = None

        # Volume
        self.slider_volume.set_command(self.changer_volume)
        self.volume = self.charger_volume()
        pygame.mixer.music.set_volume(self.volume / 100)
        self.slider_volume.set(self.volume)
        self.slider_volume.set_callback(self.changer_volume)
        if hasattr(self, "label_valeur_volume"):
            self.label_valeur_volume.config(text=str(self.volume))

        # Misc
        if root is not None:
            self.playlist_manager = PlaylistManager(self, root)
        else:
            self.playlist_manager = None

    # --------------------------------------------------------------- VOLUME
    def sauvegarder_volume(self, volume):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        data["volume"] = volume
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def charger_volume(self):
        try:
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
                return data.get("volume", 100)
        except FileNotFoundError:
            return 100
        
    def changer_volume(self, valeur):
        volume = max(0, min(float(valeur), 100)) / 100
        pygame.mixer.music.set_volume(volume)
        self.sauvegarder_volume(int(valeur))

        if hasattr(self, "label_valeur_volume"):
            self.label_valeur_volume.config(text=str(int(valeur)))

    # --------------------------------------------------------------- LECTURE / PAUSE
    def jouer_ou_pause(self, img_play, img_pause):
        if not pygame.mixer.music.get_busy() or self.en_pause:
            pygame.mixer.music.play(start=self.position_actuelle)
            pygame.mixer.music.unpause()
            self.position_depart_lecture = self.position_actuelle
            self.temps_debut_play = pygame.time.get_ticks() / 1000
            self.en_pause = False
            self.bouton_play.config(image=img_pause)
        else:
            pygame.mixer.music.pause()
            self.position_actuelle = self.get_position()
            self.en_pause = True
            self.bouton_play.config(image=img_play)

    def mettre_en_pause_temporaire(self):
        if pygame.mixer.music.get_busy():
            self.position_actuelle = self.get_position()
            self.mettre_a_jour_position()
            pygame.mixer.music.pause()
            self.en_pause_temp = True

    # --------------------------------------------------------------- DEPLACEMENT
    def mettre_a_jour_position(self):
        self.position_actuelle = self.get_position()

    def mettre_a_jour_temps_courant(self, label_courant):
        if self.en_pause_temp:
            pos = self.progression.get()
            label_courant.config(text=self.format_temps(float(pos)))

    def mettre_a_jour_progression(self, fenetre, label_courant, label_total):
        self.fenetre = fenetre
        if not self.en_pause_temp:
            pos = self.get_position()
            self.position_actuelle = pos
            self.progression.set(int(pos))
            label_courant.config(text=self.format_temps(pos))
            label_total.config(text=self.format_temps(self.duree_morceau))

            # Vérifiez si la position actuelle est proche de la fin du morceau
            if self.duree_morceau > 0 and (self.duree_morceau - pos <= 0.5):
                self.gestion_morceau_suivant()

        fenetre.after(500, lambda: self.mettre_a_jour_progression(fenetre, label_courant, label_total))

    def changer_position(self, valeur):
        if self.fichier_en_cours is None:
            return
        try:
            position = float(valeur)
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
            pygame.mixer.music.play(start=position)
            self.position_actuelle = position
            self.position_depart_lecture = position
            self.temps_debut_play = pygame.time.get_ticks() / 1000
            self.en_pause = False

            if self.img_pause:
                self.bouton_play.config(image=self.img_pause)
            self.progression.set(int(position))
        except Exception as e:
            print("Erreur lors du changement de position:", e)

    # --------------------------------------------------------------- SEEK
    def debut_seek(self, event=None):
        self.seek_en_cours_manuel = True
        self.etat_avant_seek = not self.en_pause
        pygame.mixer.music.pause()
        self.en_pause_temp = True

    def fin_seek(self, progression, event):
        nouveau_temps = progression.get()
        self.seek_en_cours_manuel = False

        if self.duree_morceau > 0 and nouveau_temps >= self.duree_morceau:
            nouveau_temps = max(0, self.duree_morceau - 0.1)
            self.progression.set(int(nouveau_temps))
        self.changer_position(nouveau_temps)
        self.en_pause_temp = False

    # --------------------------------------------------------------- MISC
    def get_position(self):
        if self.en_pause or not pygame.mixer.music.get_busy():
            return self.position_actuelle
        else:
            temps_ecoule = (pygame.time.get_ticks() / 1000) - self.temps_debut_play
            pos = self.position_depart_lecture + temps_ecoule
            return min(pos, self.duree_morceau)
        
    def format_temps(self, secondes):
        minutes = int(secondes // 60)
        secondes = int(secondes % 60)
        return f"{minutes:02d}:{secondes:02d}"
    
    def lier_labels_temps(self, fenetre, label_courant, label_total):
        self.fenetre = fenetre
        self.label_temps_courant = label_courant
        self.label_temps_total = label_total
        self.mettre_a_jour_progression(fenetre, label_courant, label_total)
        self.verifier_fin_morceau()

    def verifier_fin_morceau(self):
        position_actuelle = self.get_position()
        presque_fini = self.duree_morceau > 0 and (self.duree_morceau - position_actuelle <= 0.5)

        if (presque_fini or not pygame.mixer.music.get_busy()) and not self.en_pause:
            self.gestion_morceau_suivant()
            return

        if self.fenetre:
            self.fenetre.after(500, self.verifier_fin_morceau)

    # --------------------------------------------------------------- LOOP
    def toggle_boucle(self):
        self.etat_boucle = (self.etat_boucle + 1) % 3
        self.update_bouton_boucle()

    def update_bouton_boucle(self):
        if self.etat_boucle == BOUCLE_OFF:
            self.btn_boucle.config(image=self.img_boucle)
            self.btn_boucle.image = self.img_boucle
        elif self.etat_boucle == BOUCLE_ONCE:
            self.btn_boucle.config(image=self.img_boucle_once)
            self.btn_boucle.image = self.img_boucle_once
        elif self.etat_boucle == BOUCLE_ALWAYS:
            self.btn_boucle.config(image=self.img_boucle_always)
            self.btn_boucle.image = self.img_boucle_always
        self.btn_boucle.update_idletasks()

    def mettre_a_jour_etat_boucle(self):
        if self.etat_boucle == BOUCLE_OFF:
            self.btn_boucle.config(image=self.img_boucle)
        elif self.etat_boucle == BOUCLE_ONCE:
            self.btn_boucle.config(image=self.img_boucle_once)
        elif self.etat_boucle == BOUCLE_ALWAYS:
            self.btn_boucle.config(image=self.img_boucle_always)

    # --------------------------------------------------------------- PLAYLIST LINK
    def gestion_morceau_suivant(self):
        if self.changement_en_cours:
            return
        self.changement_en_cours = True
        if self.playlist_manager:
            self.playlist_manager.gestion_morceau_suivant(callback=self.reset_changement_flag)

    def reset_changement_flag(self):
        self.changement_en_cours = False