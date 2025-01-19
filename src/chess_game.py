import os
import pygame
from config import TAILLE_CASE, FENETRE, BLANC, NOIR, SURBRILLANCE, SURBRILLANCE_SELECTION
import chess
import time

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
        "move": "./ressources/Sounds/move-self.mp3",
        "victoire": "./ressources/Sounds/victory.mp3"  
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

class JeuEchecs:
    def __init__(self):
        self.plateau = chess.Board()
        self.images = charger_images()
        self.sons = charger_sons()
        self.case_selectionnee = None
        self.coups_possibles = []
        self.partie_terminee = False

    def jouer_son(self, action):
        if action in self.sons:
            self.sons[action].play()

    def obtenir_position_souris(self, pos):
        x, y = pos
        file = x // TAILLE_CASE
        rank = 7 - (y // TAILLE_CASE)
        return chess.square(file, rank)

    def afficher_menu_promotion(self, couleur):
        largeur = TAILLE_CASE * 4
        hauteur = TAILLE_CASE
        x = (FENETRE.get_width() - largeur) // 2
        y = (FENETRE.get_height() - hauteur) // 2
        menu_surface = pygame.Surface((largeur, hauteur))
        menu_surface.fill((200, 200, 200))
        pieces = ['dame', 'tour', 'cavalier', 'fou']
        images = []
        for piece in pieces:
            chemin = f"./ressources/Images/{couleur}_{piece}.png"
            if os.path.exists(chemin):
                image = pygame.image.load(chemin)
                image = pygame.transform.scale(image, (TAILLE_CASE, TAILLE_CASE))
                images.append(image)
            else:
                images.append(None)
        for i, image in enumerate(images):
            if image:
                menu_surface.blit(image, (i * TAILLE_CASE, 0))
        FENETRE.blit(menu_surface, (x, y))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if x <= mouse_x < x + largeur and y <= mouse_y < y + hauteur:
                        index = (mouse_x - x) // TAILLE_CASE
                        return [chess.QUEEN, chess.ROOK, chess.KNIGHT, chess.BISHOP][index]

    def gerer_clic_plateau(self, pos):
        if self.partie_terminee:
            return
        case = self.obtenir_position_souris(pos)
        if self.case_selectionnee is not None:
            if case in self.coups_possibles:
                mouvement = chess.Move(self.case_selectionnee, case)
                piece = self.plateau.piece_at(self.case_selectionnee)
                if piece.piece_type == chess.PAWN and chess.square_rank(case) in [0, 7]:
                    couleur = "blanc" if piece.color else "noir"
                    mouvement.promotion = self.afficher_menu_promotion(couleur)
                if mouvement in self.plateau.legal_moves:
                    if self.plateau.is_capture(mouvement):
                        self.jouer_son("capture")
                    else:
                        self.jouer_son("move")
                    self.plateau.push(mouvement)
                    self.verifier_fin_partie()
                self.case_selectionnee = None
                self.coups_possibles = []
            else:
                self.case_selectionnee = None
                self.coups_possibles = []
        else:
            piece = self.plateau.piece_at(case)
            if piece and piece.color == self.plateau.turn:
                self.case_selectionnee = case
                self.coups_possibles = [move.to_square for move in self.plateau.legal_moves if move.from_square == case]

    def verifier_fin_partie(self):
        if self.plateau.is_checkmate():
            self.partie_terminee = True
            self.afficher_animation_victoire("Échec et Mat !")
        elif self.plateau.is_stalemate() or self.plateau.is_insufficient_material():
            self.partie_terminee = True
            self.afficher_animation_victoire("Match nul !")

    def afficher_animation_victoire(self, message):
        self.jouer_son("victoire")
        police = pygame.font.Font(None, 80)
        couleur = (255, 215, 0)
        for _ in range(5):
            FENETRE.fill((0, 0, 0))
            texte = police.render(message, True, couleur)
            texte_rect = texte.get_rect(center=(FENETRE.get_width() // 2, FENETRE.get_height() // 2))
            FENETRE.blit(texte, texte_rect)
            pygame.display.flip()
            time.sleep(0.5)
            FENETRE.fill((0, 0, 0))
            pygame.display.flip()
            time.sleep(0.5)

    def dessiner(self):
        for y in range(8):
            for x in range(8):
                couleur = BLANC if (x + y) % 2 == 0 else NOIR
                pygame.draw.rect(FENETRE, couleur, (x * TAILLE_CASE, y * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE))
        if self.case_selectionnee is not None:
            file = chess.square_file(self.case_selectionnee)
            rank = chess.square_rank(self.case_selectionnee)
            surface = pygame.Surface((TAILLE_CASE, TAILLE_CASE), pygame.SRCALPHA)
            surface.fill(SURBRILLANCE_SELECTION)
            FENETRE.blit(surface, (file * TAILLE_CASE, (7 - rank) * TAILLE_CASE))
        for case in self.coups_possibles:
            file = chess.square_file(case)
            rank = chess.square_rank(case)
            surface = pygame.Surface((TAILLE_CASE, TAILLE_CASE), pygame.SRCALPHA)
            surface.fill(SURBRILLANCE)
            FENETRE.blit(surface, (file * TAILLE_CASE, (7 - rank) * TAILLE_CASE))
        for case in chess.SQUARES:
            piece = self.plateau.piece_at(case)
            if piece:
                image = self.images.get(piece_to_key(piece))
                if image:
                    x = chess.square_file(case) * TAILLE_CASE
                    y = (7 - chess.square_rank(case)) * TAILLE_CASE
                    FENETRE.blit(image, (x, y))
