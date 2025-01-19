import chess
from config import FENETRE, TAILLE_CASE, BLANC, NOIR, SURBRILLANCE, SURBRILLANCE_SELECTION
from assets import charger_images, piece_to_key, charger_sons
import pygame

class JeuEchecs:
    def __init__(self):
        self.plateau = chess.Board()
        self.images = charger_images()
        self.sons = charger_sons()
        self.case_selectionnee = None
        self.coups_possibles = []

    def jouer_son(self, action):
        if action in self.sons:
            self.sons[action].play()

    def obtenir_position_souris(self, pos):
        x, y = pos
        file = x // TAILLE_CASE
        rank = 7 - (y // TAILLE_CASE)
        return chess.square(file, rank)

    def gerer_clic_plateau(self, pos):
        case = self.obtenir_position_souris(pos)

        if self.case_selectionnee is not None:
            if case in self.coups_possibles:
                mouvement = chess.Move(self.case_selectionnee, case)
                if mouvement in self.plateau.legal_moves:
                    if self.plateau.is_capture(mouvement):
                        self.jouer_son("capture")
                    else:
                        self.jouer_son("move")
                    self.plateau.push(mouvement)
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