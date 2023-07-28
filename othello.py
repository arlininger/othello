"""Module for Othello game"""

import logging
import pygame

SCREEN_SIZE = 504
SCALE = SCREEN_SIZE / 8
HALF_SCALE = SCALE / 2
RADIUS = HALF_SCALE * 0.8

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255,0,0)

directions = [
    ( 1, 0),
    ( 1, 1),
    ( 0, 1),
    (-1, 1),
    (-1, 0),
    (-1,-1),
    ( 0,-1),
    ( 1,-1),
]
def add_position(base,direction):
    return tuple([sum(x) for x in zip(base,direction)])

def spaces():
    """Iterate through all spaces"""
    for x in range(8):
        for y in range(8):
            yield((x,y))


class Othello:
    """Class containing methods for othello game"""
    def __init__(self, screen):
        self.board = [["EMPTY" for x in range(8)] for x in range(8)]
        self.board[3][3] = "BLACK"
        self.board[3][4] = "WHITE"
        self.board[4][3] = "WHITE"
        self.board[4][4] = "BLACK"
        self.screen = screen
        self.turn = "WHITE"
        self.endgame = False
        self.generate_possible_moves()

    def opponent(self):
        """Get the opponent name string"""
        if self.turn == "WHITE":
            return "BLACK"
        elif self.turn == "BLACK":
            return "WHITE"
        logging.error("unknown turn")

    def draw_piece(self,coords,color):
        """Draw a specific piece at the specified coordinates"""
        screen = self.screen
        if color == "BLACK":
            draw_color = BLACK
        elif color == "WHITE":
            draw_color = WHITE
        elif color == "EMPTY":
            return
        else:
            logging.warning(f'Unknown piece color: {color} at {coords}')
        x, y = coords
        x = x * SCALE + HALF_SCALE
        y = y * SCALE + HALF_SCALE
        pygame.draw.circle(screen, draw_color, (x, y), RADIUS)

    def board_position(self,x,y=None):
        """Get piece at given position"""
        if y ==None:
            x,y = x
        if x < 0 or x >= 8 or y < 0 or y >= 8:
            return "OUT_OF_RANGE"
        return self.board[x][y]

    def is_legal_move_direction(self, move, direction, include_positions = False):
        """Determine if a move is legal for a given direction"""
        positions = list()
        temp_location = add_position(move, direction)
        if self.board_position(temp_location) != self.opponent():
            if include_positions:
                return False, []
            return False
        while self.board_position(temp_location) == self.opponent():
            positions.append(temp_location)
            temp_location = add_position(temp_location, direction)
        if self.board_position(temp_location) == self.turn:
            if include_positions:
                return True, positions
            return True
        if include_positions:
            return False, []
        return False

    def is_legal_move(self,move):
        """Determine if move is legal"""
        x,y = move
        if not self.board[x][y] == "EMPTY":
            return False
        for direction in directions:
            if self.is_legal_move_direction(move,direction):
                return True
        return False

    def generate_possible_moves(self):
        """Generate current possible moves"""
        self.current_possible_moves = list()
        for x,y in spaces():
            if self.is_legal_move((x,y)):
                self.current_possible_moves.append((x,y))

    def draw_board(self):
        """Draw the playing board"""
        screen = self.screen
        screen.fill((0, 192, 0))
        for x in range(9):
            pygame.draw.line(screen, BLACK, (0, x*SCALE), (SCREEN_SIZE, x*SCALE))
            pygame.draw.line(screen, BLACK, (x*SCALE, 0), (x*SCALE, SCREEN_SIZE))
        if self.endgame:
            pygame.draw.line(screen,RED, (0,0), (SCREEN_SIZE,SCREEN_SIZE))
            pygame.draw.line(screen,RED, (SCREEN_SIZE,0), (0,SCREEN_SIZE))

    def draw_possible_moves(self):
        """Draw possible moves"""
        screen = self.screen
        for move in self.current_possible_moves:
            corner = tuple(x * SCALE + 2 for x in move)
            size = (SCALE -3, SCALE -3)
            rect = pygame.Rect(corner, size)
            pygame.draw.rect(screen, RED,rect, 2)

    def draw(self):
        """Draw the game board"""
        self.draw_board()
        self.draw_possible_moves()

        for x in range(8):
            for y in range(8):
                self.draw_piece((x,y),self.board[x][y])

    def make_move(self,move):
        """Make a move"""
        # Make the move
        if not self.is_legal_move(move):
            return
        x,y = move
        self.board[x][y] = self.turn
        for direction in directions:
            valid,moves = self.is_legal_move_direction(move, direction, include_positions = True)
            if valid:
                for location in moves:
                    x,y = location
                    self.board[x][y] = self.turn
        # flip current player
        self.turn = self.opponent()
        self.generate_possible_moves()
        if len(self.current_possible_moves) == 0:
            self.turn = self.opponent()
            self.generate_possible_moves()
            if len(self.current_possible_moves) == 0:
                self.endgame = True
        # Get new legal moves
        # If no legal moves,
        #   flip back
        #   get new legal moves
        #   If no legal moves still, end of game






