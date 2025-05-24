# pygame va bien te faire enculer avec tes messages de bienvenue a chaque lancement

# silent_pygame_import.py
import sys
import os

# Sauvegarde des flux
sys_stdout_backup = sys.stdout
sys_stderr_backup = sys.stderr

# Redirection temporaire vers null
sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

import pygame

# Restauration
sys.stdout.close()
sys.stderr.close()
sys.stdout = sys_stdout_backup
sys.stderr = sys_stderr_backup

# Initialisation du mixer ici (en dehors du silence pour avoir les erreurs si besoin)
pygame.init()
pygame.mixer.init()