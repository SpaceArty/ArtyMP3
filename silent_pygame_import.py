# pygame va bien te faire enculer avec tes messages de bienvenue a chaque lancement

# silent_pygame_import.py
import sys
import os

# Sauvegarde des flux
old_stdout = sys.stdout
old_stderr = sys.stderr

try:
    with open(os.devnull, "w") as devnull:
        sys.stdout = devnull
        sys.stderr = devnull
        import pygame
finally:
    sys.stdout = old_stdout
    sys.stderr = old_stderr


# Initialisation du mixer ici (en dehors du silence pour avoir les erreurs si besoin)
pygame.init()
pygame.mixer.init()