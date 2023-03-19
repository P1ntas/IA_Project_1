import pygame

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE
from board import Board


pygame.init()

window_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(window_size)

fons_path = "fonts/Grand9K Pixel.ttf"
font = pygame.font.Font(fons_path, 30)

button_color = (150, 150, 150)
button_hover_color = (200, 200, 200)

button1 = font.render("Player", True, WHITE)
button1_rect = button1.get_rect(center=(window_size[0]//2, window_size[1]//3))

button2 = font.render("AI", True, WHITE)
button2_rect = button2.get_rect(center=(window_size[0]//2, window_size[1]//2))

button3 = font.render("Settings", True, WHITE)
button3_rect = button3.get_rect(center=(window_size[0]//2, 2*window_size[1]//3))

clock = pygame.time.Clock()

running = True
while running:

    screen.fill((173, 216, 230))

    pygame.draw.rect(screen, button_color, button1_rect)
    pygame.draw.rect(screen, button_color, button2_rect)
    pygame.draw.rect(screen, button_color, button3_rect)

    if button1_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, button_hover_color, button1_rect)

    if button2_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, button_hover_color, button2_rect)

    if button3_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, button_hover_color, button3_rect)

    screen.blit(button1, button1_rect)
    screen.blit(button2, button2_rect)
    screen.blit(button3, button3_rect)

    pygame.display.flip()

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if button1_rect.collidepoint(mouse_pos):
                board = Board(4, 4, screen, "player")

                board.run()

            if button2_rect.collidepoint(mouse_pos):
                print("Option 2 clicked!")

            if button3_rect.collidepoint(mouse_pos):
                print("Option 3 clicked!")
