import chess
import chess.svg
import pygame
import sys
from io import BytesIO
from pygame.locals import QUIT

import cairosvg

#https://stackoverflow.com/questions/120584/svg-rendering-in-a-pygame-application-prior-to-pygame-2-0-pygame-did-not-suppo
#https://python-forum.io/thread-40976.html


WINDOWWIDTH = 390
WINDOWHEIGHT = 390

def board_to_surface(board: chess.Board, size=390) -> pygame.Surface:
    svg_text = chess.svg.board(board=board, size=size)  # SVG text
    png_bytes = cairosvg.svg2png(bytestring=svg_text.encode("utf-8"))  # rasterize SVG -> PNG bytes
    return pygame.image.load(BytesIO(png_bytes))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    board = chess.Board()
    surface = board_to_surface(board, size=WINDOWWIDTH)

    screen.blit(surface, (0, 0))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()