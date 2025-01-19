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

def piece_to_key(piece):
    couleur = "blanc" if piece.color else "noir"
    noms = {
        chess.PAWN: "pion",
        chess.ROOK: "tour",
        chess.KNIGHT: "cavalier",
        chess.BISHOP: "fou",
        chess.QUEEN: "dame",
        chess.KING: "roi",
    }
    return f"{couleur}_{noms[piece.piece_type]}"
