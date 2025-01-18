import pygame
import chess
import sys
import os

pygame.init()

TAILLE_CASE = 70
TAILLE_PLATEAU = 8
LARGEUR_PLATEAU = TAILLE_CASE * TAILLE_PLATEAU
HAUTEUR_INTERFACE = 100  
LARGEUR = LARGEUR_PLATEAU
HAUTEUR = LARGEUR_PLATEAU + HAUTEUR_INTERFACE
TAILLE_FENETRE = (LARGEUR, HAUTEUR)
FENETRE = pygame.display.set_mode(TAILLE_FENETRE)
pygame.display.set_caption("Jeu d'Échecs")


BLANC = (240, 217, 181)
NOIR = (181, 136, 99)
SURBRILLANCE = (255, 255, 0, 100)
SURBRILLANCE_SELECTION = (0, 255, 0, 100)
MENU_FOND = (50, 50, 50)
MENU_BOUTON = (100, 149, 237)
MENU_BOUTON_HOVER = (72, 118, 255)
TEXTE_BOUTON = (255, 255, 255)


pygame.font.init()
POLICE_BOUTON = pygame.font.Font(None, 30)


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
    nom = {
        chess.PAWN: "pion",
        chess.ROOK: "tour",
        chess.KNIGHT: "cavalier",
        chess.BISHOP: "fou",
        chess.QUEEN: "dame",
        chess.KING: "roi"
    }[piece.piece_type]
    return f"{couleur}_{nom}"


class JeuEchecs:
    def __init__(self):
        self.plateau = chess.Board()
        self.images = charger_images()
        self.case_selectionnee = None
        self.coups_possibles = []

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
        for y in range(TAILLE_PLATEAU):
            for x in range(TAILLE_PLATEAU):
                couleur = BLANC if (x + y) % 2 == 0 else NOIR
                pygame.draw.rect(FENETRE, couleur,
                                 (x * TAILLE_CASE, y * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE))

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


def dessiner_interface(boutons):

    pygame.draw.rect(FENETRE, MENU_FOND, (0, LARGEUR_PLATEAU, LARGEUR, HAUTEUR_INTERFACE))

    
    for rect, texte in boutons:
        souris = pygame.mouse.get_pos()
        if rect.collidepoint(souris):
            pygame.draw.rect(FENETRE, MENU_BOUTON_HOVER, rect)
        else:
            pygame.draw.rect(FENETRE, MENU_BOUTON, rect)
        pygame.draw.rect(FENETRE, TEXTE_BOUTON, rect, 2)  

        texte_surface = POLICE_BOUTON.render(texte, True, TEXTE_BOUTON)
        texte_rect = texte_surface.get_rect(center=rect.center)
        FENETRE.blit(texte_surface, texte_rect)


def main():
    jeu = JeuEchecs()
    clock = pygame.time.Clock()

    
    boutons = []
    largeur_bouton = 170
    hauteur_bouton = 50
    espace = 15
    x_offset = (LARGEUR - (3 * largeur_bouton + 2 * espace)) // 2
    y_offset = LARGEUR_PLATEAU + (HAUTEUR_INTERFACE - hauteur_bouton) // 2

    for i, texte in enumerate(["Recommencer", "Quitter"]):
        rect = pygame.Rect(x_offset + i * (largeur_bouton + espace), y_offset, largeur_bouton, hauteur_bouton)
        boutons.append((rect, texte))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    for rect, action in boutons:
                        if rect.collidepoint(event.pos):
                            if action == "Recommencer":
                                jeu = JeuEchecs()  
                            elif action == "Quitter":
                                pygame.quit()
                                sys.exit()

                    
                    if event.pos[1] < LARGEUR_PLATEAU:
                        jeu.gerer_clic_plateau(event.pos)

        
        FENETRE.fill((0, 0, 0))
        jeu.dessiner()
        dessiner_interface(boutons)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
