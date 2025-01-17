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

# Charger les images des pièces
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

# Charger l'image pour les cases vides
piece_images['.'] = pygame.image.load("Images/Empty.png")
piece_images['.'] = pygame.transform.scale(piece_images['.'], (square_size, square_size))

Screen = pygame.display.set_mode((width, height))
Screen.fill(white)
pygame.display.set_caption("Chess")

def draw_board():
    for row in range(8):
        for col in range(8):
            rect = pygame.Rect(col * square_size, row * square_size, square_size, square_size)
            if (row + col) % 2 == 0:
                pygame.draw.rect(Screen, color1, rect)
            else:
                pygame.draw.rect(Screen, color2, rect)

def draw_pieces(board):
    board_str = str(board).split('\n')
    for row_idx, row in enumerate(board_str):
        for col_idx, cell in enumerate(row.split()):
            Screen.blit(piece_images.get(cell, piece_images['.']), (col_idx * square_size, row_idx * square_size))

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

board = chess.Board()

# Charger les images des pièces
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

# Charger l'image pour les cases vides
piece_images['.'] = pygame.image.load("Images/Empty.png")
piece_images['.'] = pygame.transform.scale(piece_images['.'], (square_size, square_size))

Screen = pygame.display.set_mode((width, height))
Screen.fill(white)
pygame.display.set_caption("Chess")

selected_square = None

def draw_board():
    for row in range(8):
        for col in range(8):
            rect = pygame.Rect(col * square_size, row * square_size, square_size, square_size)
            if (row + col) % 2 == 0:
                pygame.draw.rect(Screen, color1, rect)
            else:
                pygame.draw.rect(Screen, color2, rect)

    if selected_square is not None:
        selected_rect = pygame.Rect(selected_square[1] * square_size, selected_square[0] * square_size, square_size, square_size)
        pygame.draw.rect(Screen, black, selected_rect, 5)

def draw_pieces(board):
    board_str = str(board).split('\n')
    for row_idx, row in enumerate(board_str):
        for col_idx, cell in enumerate(row.split()):
            Screen.blit(piece_images.get(cell, piece_images['.']), (col_idx * square_size, row_idx * square_size))

def handle_click(board, pos):
    global selected_square
    col = pos[0] // square_size
    row = pos[1] // square_size

    column_letter = chr(ord('a') + col)
    row_number = 8 - row
    cell_name = f"{column_letter}{row_number}"

    board_str = str(board).split('\n')
    value = board_str[row].split()[col]
    if value == '.':
        move = chess.Move.from_uci(convert_cell_name(selected_square) + cell_name)
        if board.is_legal(move):
            board.push(move)
            selected_square = None
        else:
            selected_square = (row, col)
    else:
        selected_square = (row, col)

def convert_cell_name(cell):
    column_letter = chr(ord('a') + cell[1])
    row_number = 8 - cell[0]
    cell_name = f"{column_letter}{row_number}"
    return cell_name

while True:

    for event in pygame.event.get():              
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            handle_click(board, event.pos)

    draw_board()
    draw_pieces(board)

    pygame.display.update()
    FramePerSec.tick(FPS)