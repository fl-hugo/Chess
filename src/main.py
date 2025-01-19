import sys
import pygame
from config import FENETRE, LARGEUR_PLATEAU, HAUTEUR_INTERFACE, LARGEUR, HAUTEUR
from chess_game import JeuEchecs
from ui import dessiner_interface

def main():
    pygame.init()
    clock = pygame.time.Clock()
    jeu = JeuEchecs()

    boutons = []
    largeur_bouton = 120
    hauteur_bouton = 50
    espace = 15
    x_offset = (LARGEUR - (3 * largeur_bouton + 2 * espace)) // 2
    y_offset = LARGEUR_PLATEAU + (HAUTEUR_INTERFACE - hauteur_bouton) // 2

    for i, texte in enumerate(["Recommencer", "Problèmes", "Quitter"]):
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
                            elif action == "Problèmes":
                                jeu.demarrer_probleme()
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