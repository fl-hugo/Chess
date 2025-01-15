import pygame, sys
from pygame.locals import *
import chess

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

white = (255, 255, 255)
black = (0, 0, 0)
color1 = (250,216,165)
color2 = (144,96,26)
width = 800
height = 800
square_size = width // 8

piece_images = {}
piece_map = {
    'P': 'WhitePawn',
    'R': 'WhiteRook',
    'N': 'WhiteKnight',
    'B': 'WhiteBishop',
    'Q': 'WhiteQueen',
    'K': 'WhiteKing',
    'p': 'BlackPawn',
    'r': 'BlackRook',
    'n': 'BlackKnight',
    'b': 'BlackBishop',
    'q': 'BlackQueen',
    'k': 'BlackKing'
}
for piece, image_name in piece_map.items():
    piece_images[piece] = pygame.image.load(f"Images/{image_name}.png")
    piece_images[piece] = pygame.transform.scale(piece_images[piece], (square_size, square_size))

Screen = pygame.display.set_mode((width, height))
Screen.fill(white)
pygame.display.set_caption("Chess")

def draw_board():
    """Dessine la grille de l'échiquier."""
    for row in range(8):
        for col in range(8):
            rect = pygame.Rect(col * square_size, row * square_size, square_size, square_size)
            if (row + col) % 2 == 0:
                pygame.draw.rect(Screen, color1, rect)
            else:
                pygame.draw.rect(Screen, color2, rect)

def draw_pieces(board):
    """Place les pièces sur la grille selon la variable board."""
    board_str = str(board).split('\n')
    for row_idx, row in enumerate(board_str):
        for col_idx, cell in enumerate(row.split()):
            if cell != '.':
                Screen.blit(piece_images[cell], (col_idx * square_size, row_idx * square_size))

while True:
    board = chess.Board()
    
    for event in pygame.event.get():              
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    draw_board()
    draw_pieces(board)

    pygame.display.update()
    FramePerSec.tick(FPS)