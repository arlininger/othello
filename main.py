#!/usr/bin/env python3

import logging
import pygame
from othello import Othello
import ai_none
import ai_random

SCREEN_SIZE = 504
SCALE = SCREEN_SIZE / 8
HALF_SCALE = SCALE / 2
RADIUS = HALF_SCALE * 0.8

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

UserAI = ai_none.NoAI()
next_move = {"WHITE" : UserAI, "BLACK" : ai_random.RandomAI()}


def main():
    """Main Program"""
    pygame.init()

    # Set up the drawing window
    screen = pygame.display.set_mode([SCREEN_SIZE, SCREEN_SIZE])

    # Run until the user asks to quit
    running = True
    game = Othello(screen)
    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                y = int(y // SCALE)
                x = int(x // SCALE)
                UserAI.set_move((x,y))

        current_ai = next_move[game.turn]
        move = current_ai.get_move(game)
        if move:
            game.make_move(move)
        game.draw()
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()

if __name__ == '__main__':
    main()
