#https://stackoverflow.com/questions/120584/svg-rendering-in-a-pygame-application-prior-to-pygame-2-0-pygame-did-not-suppo
#https://python-forum.io/thread-40976.html

import chess
import chess.svg
import pygame
import sys
from io import BytesIO # standard lib
from pygame.locals import *

WINDOWWIDTH = 390
WINDOWHEIGHT = 390

board = chess.Board() 
print(board)
svg_text = chess.svg.board(board)
 
svg_bytes = bytes(svg_text, encoding='utf-8')
bytestream = BytesIO(svg_bytes) # or "with BytesIO(svg_bytes) as bytestream: ..."
surface = pygame.image.load(bytestream)



def main():
    temps = 0
    pygame.init()
    screen = pygame.display.set_mode((WINDOWHEIGHT,WINDOWWIDTH))
    
    screen.blit(surface, (0,0))
    
    pygame.display.update()
    
    
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()

main()