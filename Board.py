import pygame
from Tile import Tile

# Game state checker
class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tile_width = width // 8
        self.tile_height = height // 8
        self.selected_piece = None
        self.config = [
            ['','','',''],
            ['','','',''],
            ['','','',''],
            ['','','',''],
        ]
        self.tiles = self.generate_tiles()
        self.setup_board()

    def generate_tiles(self):
        output = []
        for y in range(8):
            for x in range(8):
                output.append(
                    Tile(x,  y, self.tile_width, self.tile_height)
                )
        return output

    def get_tile_from_pos(self, pos):
        for tile in self.tiles:
            if (tile.x, tile.y) == (pos[0], pos[1]):
                return tile

    def get_piece_from_pos(self, pos):
        return self.get_tile_from_pos(pos).occupying_piece
    
    def setup_board(self):
        for y, row in enumerate(self.config):
            for x, piece in enumerate(row):
                if piece != '':
                    tile = self.get_tile_from_pos((x, y))
                    # looking inside contents, what piece does it have
                    if piece[1] == 'R':
                        tile.occupying_piece = Piece((x, y), 'red', self)
                    # as you notice above, we put `self` as argument, or means our class Board
                    elif piece[1] == 'G':
                        tile.occupying_piece = Piece((x, y), 'green', self)
                    elif piece[1] == 'B':
                        tile.occupying_piece = Piece((x, y), 'blue', self)
                    elif piece[1] == 'O':
                        tile.occupying_piece = Piece((x, y), 'orange', self)

    def handle_click(self, mx, my):
        x = mx // self.tile_width
        y = my // self.tile_height
        clicked_tile = self.get_tile_from_pos((x, y))
        if self.selected_piece is None:
            if clicked_tile.occupying_piece is not None:
                self.selected_piece = clicked_tile.occupying_piece
        elif clicked_tile.occupying_piece is not None:
                self.selected_piece = clicked_tile.occupying_piece

     # check state checker
    def win_condition(self, board_change=None): # board_change = [(x1, y1), (x2, y2)]
        win = True
        changing_piece = None
        old_tile = None
        new_tile = None
        new_tile_old_piece = None
        pieces = [
            i.occupying_piece for i in self.tiles if i.occupying_piece is not None
        ]
        if board_change is not None:
            for tile in self.tiles:
                if tile.pos == board_change[0]:
                    changing_piece = tile.occupying_piece
                    old_tile = tile
                    old_tile.occupying_piece = None
            for tile in self.tiles:
                if tile.pos == board_change[1]:
                    new_tile = tile
                    new_tile_old_piece = new_tile.occupying_piece
                    new_tile.occupying_piece = changing_piece
        for piece in pieces:
            if not piece.joined:
                win = False
        if board_change is not None:
            old_tile.occupying_piece = changing_piece
            new_tile.occupying_piece = new_tile_old_piece
        return win
    
    def draw(self, display):
        if self.selected_piece is not None:
            self.get_tile_from_pos(self.selected_piece.pos).highlight = True
            for tile in self.selected_piece.get_valid_moves(self):
                tile.highlight = True
        for tile in self.tiles:
            tile.draw(display)