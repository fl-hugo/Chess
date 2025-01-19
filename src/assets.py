import os
import pygame
from config import TAILLE_CASE
import chess

def charger_images():
    pieces = {}
    for couleur in ['blanc', 'noir']:
        for piece in ['pion', 'tour', 'cavalier', 'fou', 'dame', 'roi']:
            chemin = f"./ressources/Images/{couleur}_{piece}.png"
            if os.path.exists(chemin):
                image = pygame.image.load(chemin)
                image = pygame.transform.scale(image, (TAILLE_CASE, TAILLE_CASE))
                pieces[f"{couleur}_{piece}"] = image
            else:
                print(f"Image non trouvée: {chemin}")
    return pieces

def charger_sons():
    sons = {}
    fichiers_sons = {
        "capture": "./ressources/Sounds/capture.mp3",
        "move": "./ressources/Sounds/move-self.mp3"
    }
    for nom, chemin in fichiers_sons.items():
        if os.path.exists(chemin):
            try:
                sons[nom] = pygame.mixer.Sound(chemin)
            except pygame.error as e:
                print(f"Erreur lors du chargement du son '{nom}': {e}")
        else:
            print(f"Fichier audio non trouvé: {chemin}")
    return sons
