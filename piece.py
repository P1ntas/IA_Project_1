import pygame

from constants import TILE_SIZE


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
