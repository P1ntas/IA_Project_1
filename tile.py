import pygame

from constants import CELL_SIZE, TILE_SIZE, BLACK, CREAM

class Tile:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.has_piece = False
        self.color = CREAM
        self.tile_rect = pygame.Rect(col * CELL_SIZE + 1, row * CELL_SIZE + 1, TILE_SIZE - 2, TILE_SIZE - 2)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.tile_rect)
        pygame.draw.rect(surface, BLACK, self.tile_rect, 1)
