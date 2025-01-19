import pygame
from config import FENETRE, MENU_FOND, MENU_BOUTON, MENU_BOUTON_HOVER, TEXTE_BOUTON, POLICE_BOUTON

def dessiner_interface(boutons):
    pygame.draw.rect(FENETRE, MENU_FOND, (0, 560, 560, 100))

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
