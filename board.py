import sys
import random
import pygame

from constants import *
from tile import Tile
from piece import Piece
from solver import Solver
from copy import deepcopy


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
        self.all_moves = []

    def create_pieces(self):
        pieces = [
            Piece(BLUE, 0, 0),
            Piece(BLUE, 1, 1),
            Piece(BLUE, 2, 2),
            Piece(GREEN, 3, 3),
            Piece(GREEN, 1, 3),
            Piece(GREEN, 0, 2),
            Piece(RED, 0, 3),
            Piece(RED, 1, 2),
            Piece(RED, 3, 0)
        ]
        for piece in pieces:
            self.tiles[piece.row][piece.col].has_piece = True
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
                        self.all_moves.append((self.selected_tile.row, self.selected_tile.col, row, col))
                    self.selected_tile = None
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
        mode = self.mode
        if mode == "minimax":
            self.run_minimax()
        elif mode == "bfs":
            self.run_bfs()
        elif mode == "astar":
            self.run_astar()
        elif mode =="greedy":
            self.run_greedy()

        else:
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
        if self.selected_tile is None:
            return False
        self.selected_tile = self.tiles[move[0]][move[1]]
        piece = next((piece for piece in self.pieces if
            piece.row == self.selected_tile.row and piece.col == self.selected_tile.col), None)


        if piece is None:
            return False

        if not self.can_move_piece(piece, move[0], move[1]):
            return False

        self.tiles[piece.row][piece.col].has_piece = False
        self.all_moves.append((self.selected_tile.row, self.selected_tile.col, move[0], move[1]))
        piece.row = move[0]
        piece.col = move[1]
        self.tiles[piece.row][piece.col].has_piece = True

        self.selected_tile = self.tiles[piece.row][piece.col]
        return True


    def undo_move(self):
        if len(self.all_moves) == 0:
            return
        last_move = self.all_moves.pop()
        from_row, from_col, to_row, to_col = last_move
        piece = next((piece for piece in self.pieces if piece.row == to_row and piece.col == to_col), None)
        if piece:
            piece.row, piece.col = from_row, from_col
            self.tiles[from_row][from_col].has_piece = True
            self.tiles[to_row][to_col].has_piece = False
            self.moves -= 1
            self.check_joined_pieces()

    
    def get_first_tile(self):
        for row in range(self.height):
            for col in range(self.width):
                if self.tiles[row][col].has_piece:
                    piece = next((piece for piece in self.pieces if piece.row == row and piece.col == col), None)
                    if piece and not piece.joined:
                        return self.tiles[row][col]
        return None

                
    def get_last_move(self):
        if len(self.all_moves) == 0:
            return None
        return self.all_moves[-1][0], self.all_moves[-1][1]
    
    #Make a function that copies the board and returns it
    def copy(self):
        copy = Board(self.width, self.height, self.screen, self.mode)
        copy.tiles = deepcopy(self.tiles)
        copy.pieces = deepcopy(self.pieces)
        copy.piece_selected = deepcopy(self.piece_selected)
        copy.selected_tile = deepcopy(self.selected_tile)
        copy.moves = deepcopy(self.moves)
        copy.all_moves = deepcopy(self.all_moves)
        return copy

    def run_minimax(self):
        self.selected_tile = self.get_first_tile()
        solver = Solver(self)
        while True:
            self.selected_tile = self.get_first_tile()
            
            if self.win_condition():
                self.draw_win_screen()
                pygame.time.delay((3 * 1000))
                pygame.quit()
                sys.exit()

            move, _ = solver.minimax(5, True) # get the best move from minimax with depth 5
            if move is None:
                pygame.time.delay((3 * 1000))
                pygame.quit()
                sys.exit()
            self.make_move(move) # make the best move
            self.draw(self.screen) # draw the board after each move
            pygame.display.flip() # update the screen
            pygame.time.delay(500) # add a small delay between each move

    def run_bfs(self):
        self.selected_tile = self.get_first_tile()
        solver = Solver(self)

        best_path, nodes_explored = solver.bfs(self)  # get the best move from bfs with depth 5

        if best_path is None:
            pygame.time.delay((3 * 1000))
            pygame.quit()
            sys.exit()
        else:
            for move in best_path:
                self.make_move(move)
                self.draw(self.screen)
                pygame.display.flip()
                pygame.time.delay(500)


    def run_greedy(self):
        self.selected_tile = self.get_first_tile()
        aux = self.copy()
        solver = Solver(aux)
        
        moves = solver.greedy(aux) # get the best move using the greedy algorithm
        if moves is None:
            pygame.time.delay((3 * 1000))
            pygame.quit()
            sys.exit()
        
        else:
            for move in moves:
                self.make_move(move)
                self.draw(self.screen)
                pygame.display.flip()
                pygame.time.delay(500)

