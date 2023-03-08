# /* Piece.py

import pygame

class Piece:
    def __init__(self, pos, color, board):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.joined = False
        self.color = color
        self.has_moved = False  

    def get_moves(self, board):
        output = []
        for direction in self.get_possible_moves(board):
            for tile in direction:
                if tile.occupying_piece is not None:
                    output.append(tile)
        return output
    
    def get_valid_moves(self, board):
        output = []
        for tile in self.get_moves(board):
            if not board.win_condition(board_change=[self.pos, tile.pos]):
                output.append(tile)
        return output
    
    def move(self, board, tile, force=False):
        for i in board.tiles:
            i.highlight = False
        if tile in self.get_valid_moves(board) or force:
            prev_tile = board.get_tile_from_pos(self.pos)
            self.pos, self.x, self.y = tile.pos, tile.x, tile.y
            prev_tile.occupying_piece = None
            tile.occupying_piece = self
            board.selected_piece = None
            self.has_moved = True
        else:
            board.selected_piece = None
            return False
    
    def get_possible_moves(self, board):
        output = []
        moves = [
            (0,-1), # north
            (1, 0), # east
            (0, 1), # south
            (-1, 0), # west
        ]
        for move in moves:
            new_pos = (self.x + move[0], self.y + move[1])
            if (
                new_pos[0] < 4 and
                new_pos[0] >= 0 and 
                new_pos[1] < 4 and 
                new_pos[1] >= 0
            ):
                output.append([
                    board.get_tile_from_pos(
                        new_pos
                    )
                ])
        return output
    
    def can_be_joined(self, board):
        for tile in self.get_moves(board):
            if tile.occupying_piece is not None and tile.occupying_piece.color is self.color:
                return True
        return False
