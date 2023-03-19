import sys
import random
import pygame

from constants import *
from tile import Tile
from piece import Piece


class Board:
    def __init__(self, width, height, screen, mode):
        self.width = width
        self.height = height
        self.screen = screen
        self.mode = mode
        self.tiles = [[Tile(row, col) for col in range(width)] for row in range(height)]
        self.selected_tile = None
        self.pieces = self.create_pieces()
        self.piece_selected = False
        self.moves = 0

    def create_pieces(self):
        tiles = random.sample([(row, col) for row in range(4) for col in range(4)], 9)
        random.shuffle(tiles)
        pieces = []
        for i, tile in enumerate(tiles):
            if i < 3:
                color = BLUE
            elif i < 6:
                color = GREEN
            else:
                color = RED
            row, col = tile
            piece = Piece(color, row, col)
            pieces.append(piece)
            self.tiles[row][col].has_piece = True
        return pieces

    def draw(self, surface):
        surface.fill(BLACK)
        for row in range(self.height):
            for col in range(self.width):
                self.tiles[row][col].draw(surface)
                if self.tiles[row][col].has_piece:
                    piece = next((piece for piece in self.pieces if piece.row == row and piece.col == col), None)
                    if piece:
                        piece.draw(surface)

                        if self.piece_selected and self.selected_tile is not None:
                            possible_moves = self.get_possible_moves()
                            if (piece.row, piece.col) == (self.selected_tile.row, self.selected_tile.col):
                                for move in possible_moves:
                                    x = move[0]
                                    y = move[1]
                                    self.tiles[x][y].color = YELLOW
                                    self.tiles[x][y].draw(surface)

    def handle_event(self, event):
        self.check_joined_pieces()
        if event.type == pygame.MOUSEBUTTONDOWN:
            row, col = event.pos[1] // CELL_SIZE, event.pos[0] // CELL_SIZE
            if self.selected_tile is None:
                if self.tiles[row][col].has_piece:
                    self.selected_tile = self.tiles[row][col]
                    self.piece_selected = True
            else:
                if self.selected_tile.row == row and self.selected_tile.col == col:
                    self.selected_tile = None
                    self.piece_selected = False
                elif not self.tiles[row][col].has_piece:
                    piece = next((piece for piece in self.pieces if
                                  piece.row == self.selected_tile.row and piece.col == self.selected_tile.col), None)
                    if piece and self.can_move_piece(piece, row, col):
                        piece.row, piece.col = row, col
                        self.tiles[row][col].has_piece = True
                        self.tiles[self.selected_tile.row][self.selected_tile.col].has_piece = False
                        self.piece_selected = False
                        self.moves += 1
                    self.selected_tile = None

        for x in self.tiles:
            for possible_tile in x:
                if possible_tile.color == YELLOW:
                    possible_tile.color = CREAM

    def can_move_piece(self, piece, row, col):
        if piece.joined:
            return False
        if (abs(row - piece.row) == 1 and col == piece.col) or (abs(col - piece.col) == 1 and row == piece.row):
            if not self.tiles[row][col].has_piece:
                return True
        return False

    def get_possible_moves(self):
        if self.selected_tile is None:
            return []

        possible_moves = []
        piece = next((piece for piece in self.pieces if
                      piece.row == self.selected_tile.row and piece.col == self.selected_tile.col), None)

        if piece is None:
            return []

        for row in range(self.height):
            for col in range(self.width):
                if not self.tiles[row][col].has_piece and self.can_move_piece(piece, row, col):
                    possible_moves.append((row, col))

        return possible_moves

    def check_joined_pieces(self):
        for piece1 in self.pieces:
            for piece2 in self.pieces:
                if piece1 != piece2 and piece1.color == piece2.color:
                    if (piece1.row == piece2.row and abs(piece1.col - piece2.col) == 1) or \
                            (piece1.col == piece2.col and abs(piece1.row - piece2.row) == 1):
                        piece1.joined = True
                        piece2.joined = True

    def win_condition(self):
        joined_pieces = [piece for piece in self.pieces if piece.joined]
        if len(joined_pieces) == len(self.pieces):
            return True
        return False

    def draw_win_screen(self):
        self.screen.fill((0, 0, 0))
        font_path = "fonts/Grand9K Pixel.ttf"
        font = pygame.font.Font(font_path, 40)
        title = font.render('You Won!', True, (255, 255, 255))
        moves_button = font.render('Moves = ' + str(self.moves), True, (255, 255, 255))
        self.screen.blit(title, (SCREEN_WIDTH / 2 - title.get_width() / 2, SCREEN_WIDTH / 2 - title.get_height() / 3 - 40))
        self.screen.blit(moves_button, (SCREEN_WIDTH / 2 - moves_button.get_width() / 2, SCREEN_HEIGHT / 1.9 + moves_button.get_height() - 30))
        pygame.display.update()

    def run(self):
        while True:
            if self.win_condition():
                self.draw_win_screen()
                pygame.time.delay((3 * 1000))
                pygame.quit()
                sys.exit()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                else:
                    self.handle_event(event)

            self.draw(self.screen)

            pygame.display.flip()

    def make_move(self, move):
        return

    def undo_move(self, move):
        return
