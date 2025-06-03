import os, sys, json

class SettingsManager:
    def __init__(self, app_name="ArtyMP3", default_file="settings.json"):
        self.app_name = app_name
        self.default_file = default_file
        self.settings_path = self.get_user_settings_path()
        self.settings = self.load_settings()
        self.BOUCLE_OFF = self.get('BOUCLE_OFF', 0)
        self.BOUCLE_ONCE = self.get('BOUCLE_ONCE', 1)
        self.BOUCLE_ALWAYS = self.get('BOUCLE_ALWAYS', 2)

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def get_user_settings_path(self):
        appdata = os.getenv("APPDATA")
        dossier = os.path.join(appdata, self.app_name)
        os.makedirs(dossier, exist_ok=True)
        return os.path.join(dossier, self.default_file)

    def load_settings(self):
        # Charge les paramètres utilisateur s'ils existent
        if os.path.exists(self.settings_path):
            try:
                with open(self.settings_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("[⚠] JSON utilisateur corrompu, chargement des defaults.")

        # Sinon charge les paramètres par défaut
        try:
            default_path = self.resource_path(self.default_file)
            with open(default_path, "r", encoding="utf-8") as f:
                defaults = json.load(f)
            # Sauvegarde par défaut dans le fichier utilisateur
            with open(self.settings_path, "w", encoding="utf-8") as f:
                json.dump(defaults, f, indent=4)
            return defaults
        except Exception as e:
            print(f"[⚠] Erreur chargement defaults : {e}")
            return {}

    def save_settings(self):
        try:
            with open(self.settings_path, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=4)
            self.afficher_tous_les_parametres()
        except Exception as e:
            print(f"[⚠] Erreur lors de la sauvegarde : {e}")

    def afficher_tous_les_parametres(self):
        print("\n[📋] Paramètres actuels :")
        if not self.settings:
            print("  (aucun paramètre trouvé)")
        for cle, valeur in self.settings.items():
            print(f"  {cle} = {valeur}")

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value
        self.save_settings()
    
    def get_volume(self):
        return self.get("volume", 100)  # valeur par défaut 100

    def set_volume(self, volume):
        volume = max(0, min(int(volume), 100))
        self.settings["volume"] = volume
        self.save_settings()