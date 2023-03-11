import sys
import random
import pygame


# Define constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
CELL_SIZE = 100
TILE_SIZE = 100

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


# Define tile class
class Tile:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.has_piece = False
        self.color = WHITE
        self.tile_rect = pygame.Rect(col * CELL_SIZE + 1, row * CELL_SIZE + 1, TILE_SIZE - 2, TILE_SIZE - 2)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.tile_rect)
        pygame.draw.rect(surface, BLACK, self.tile_rect, 1)


class Piece:
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col
        self.joined = False

    def draw(self, surface):
        x = self.col * TILE_SIZE
        y = self.row * TILE_SIZE
        pygame.draw.rect(surface, self.color, (x, y, TILE_SIZE - 2, TILE_SIZE - 2))


# Define board class
class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [[Tile(row, col) for col in range(width)] for row in range(height)]
        self.selected_tile = None
        self.pieces = self.create_pieces()
        self.piece_selected = False

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
                    self.selected_tile = None

        for x in self.tiles:
            for t in x:
                if t.color == YELLOW:
                    t.color = WHITE

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

    def run(self):
        while True:
            if self.win_condition():
                
                pygame.quit()
                sys.exit()
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                else:
                    self.handle_event(event)

            # Draw grid
            self.draw(screen)

            # Update screen
            pygame.display.flip()

            # Set framerate
            clock.tick(60)

# Initialize board
board = Board(4, 4)

# Run game
board.run()
