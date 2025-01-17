import pygame
import chess
import sys
import os

pygame.init()

TAILLE_CASE = 70
TAILLE_PLATEAU = 8
LARGEUR = HAUTEUR = TAILLE_CASE * TAILLE_PLATEAU
TAILLE_FENETRE = (LARGEUR, HAUTEUR)
FENETRE = pygame.display.set_mode(TAILLE_FENETRE)
pygame.display.set_caption("Jeu d'Échecs")

BLANC = (255, 255, 255)
NOIR = (128, 128, 128)
SURBRILLANCE = (255, 255, 0, 50)
SURBRILLANCE_SELECTION = (0, 255, 0, 50)
MENU_FOND = (200, 200, 200)
MENU_BORDURE = (100, 100, 100)

class MenuPromotion:
    def __init__(self, couleur, position):
        self.couleur = couleur
        self.position = position
        self.pieces = [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]
        self.hauteur_menu = TAILLE_CASE * len(self.pieces)
        self.rect = pygame.Rect(
            position[0] * TAILLE_CASE,
            min((7 - position[1]) * TAILLE_CASE, HAUTEUR - self.hauteur_menu),
            TAILLE_CASE,
            self.hauteur_menu
        )

    def dessiner(self, fenetre, images):
        pygame.draw.rect(fenetre, MENU_FOND, self.rect)
        pygame.draw.rect(fenetre, MENU_BORDURE, self.rect, 2)

        for i, piece_type in enumerate(self.pieces):
            piece = chess.Piece(piece_type, self.couleur)
            image = images.get(piece_to_key(piece))
            if image:
                fenetre.blit(image, (self.rect.x, self.rect.y + i * TAILLE_CASE))

    def get_piece_at_pos(self, pos):
        if not self.rect.collidepoint(pos):
            return None
        
        y_relatif = pos[1] - self.rect.y
        index = y_relatif // TAILLE_CASE
        if 0 <= index < len(self.pieces):
            return self.pieces[index]
        return None

def charger_images():
    pieces = {}
    for couleur in ['blanc', 'noir']:
        for piece in ['pion', 'tour', 'cavalier', 'fou', 'dame', 'roi']:
            chemin = f"Images/{couleur}_{piece}.png"
            if os.path.exists(chemin):
                image = pygame.image.load(chemin)
                image = pygame.transform.scale(image, (TAILLE_CASE, TAILLE_CASE))
                pieces[f"{couleur}_{piece}"] = image
            else:
                print(f"Image non trouvée: {chemin}")
    return pieces

def piece_to_key(piece):
    """Convertit une pièce python-chess en clé pour le dictionnaire d'images"""
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
        self.menu_promotion = None
        self.mouvement_en_attente = None

    def obtenir_position_souris(self, pos):
        x, y = pos
        file = x // TAILLE_CASE
        rank = 7 - (y // TAILLE_CASE)
        return chess.square(file, rank)

    def est_promotion(self, depart, arrivee):
        piece = self.plateau.piece_at(depart)
        return (piece is not None and piece.piece_type == chess.PAWN and 
                ((piece.color and chess.square_rank(arrivee) == 7) or 
                 (not piece.color and chess.square_rank(arrivee) == 0)))

    def gerer_clic(self, pos):
        if self.menu_promotion:
            piece_promotion = self.menu_promotion.get_piece_at_pos(pos)
            if piece_promotion:
                depart, arrivee = self.mouvement_en_attente
                mouvement = chess.Move(depart, arrivee, promotion=piece_promotion)
                self.plateau.push(mouvement)
                self.menu_promotion = None
                self.mouvement_en_attente = None
                self.verifier_fin_partie()
            return

        case = self.obtenir_position_souris(pos)
        
        if self.case_selectionnee is not None:
            if case in self.coups_possibles:
                if self.est_promotion(self.case_selectionnee, case):
                    self.mouvement_en_attente = (self.case_selectionnee, case)
                    self.menu_promotion = MenuPromotion(
                        self.plateau.turn,
                        (chess.square_file(case), chess.square_rank(case))
                    )
                else:
                    mouvement = chess.Move(self.case_selectionnee, case)
                    self.plateau.push(mouvement)
                    self.verifier_fin_partie()

            self.case_selectionnee = None
            self.coups_possibles = []
            
        else:
            piece = self.plateau.piece_at(case)
            if piece and piece.color == self.plateau.turn:
                self.case_selectionnee = case
                self.coups_possibles = [move.to_square for move in self.plateau.legal_moves 
                                      if move.from_square == case]

    def verifier_fin_partie(self):
        if self.plateau.is_game_over():
            resultat = self.plateau.outcome()
            if resultat:
                print("Partie terminée !")
                if resultat.winner is not None:
                    print("Les Blancs gagnent !" if resultat.winner else "Les Noirs gagnent !")
                else:
                    print("Match nul !")

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

        if self.menu_promotion:
            self.menu_promotion.dessiner(FENETRE, self.images)

def main():
    if not os.path.exists('images'):
        os.makedirs('images')
        print("Veuillez placer les images des pièces dans le dossier 'images' avec le format:")
        print("blanc_pion.png, blanc_tour.png, blanc_cavalier.png, etc.")
        print("noir_pion.png, noir_tour.png, noir_cavalier.png, etc.")

    jeu = JeuEchecs()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    jeu.gerer_clic(event.pos)

        FENETRE.fill(BLANC)
        jeu.dessiner()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()