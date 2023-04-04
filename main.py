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
                if button2_rect.collidepoint(mouse_pos):
                    # Create a new menu with the AI options
                    ai_menu_font = pygame.font.Font(fons_path, 30)

                    ai_button1 = ai_menu_font.render("BFS", True, WHITE)
                    ai_button1_rect = ai_button1.get_rect(center=(window_size[0]//2, window_size[1]//3))

                    ai_button2 = ai_menu_font.render("Minimax", True, WHITE)
                    ai_button2_rect = ai_button2.get_rect(center=(window_size[0]//2, window_size[1]//2))

                    ai_button3 = ai_menu_font.render("Iterative Deepening", True, WHITE)
                    ai_button3_rect = ai_button3.get_rect(center=(window_size[0]//2, 2*window_size[1]//3))

                    ai_button4 = ai_menu_font.render("A Star", True, WHITE)
                    ai_button4_rect = ai_button4.get_rect(center=(window_size[0]//2, 5*window_size[1]//6))

                    # Run the new AI menu
                    ai_menu_running = True
                    while ai_menu_running:

                        screen.fill((173, 216, 230))

                        pygame.draw.rect(screen, button_color, ai_button1_rect)
                        pygame.draw.rect(screen, button_color, ai_button2_rect)
                        pygame.draw.rect(screen, button_color, ai_button3_rect)
                        pygame.draw.rect(screen, button_color, ai_button4_rect)

                        if ai_button1_rect.collidepoint(pygame.mouse.get_pos()):
                            pygame.draw.rect(screen, button_hover_color, ai_button1_rect)

                        if ai_button2_rect.collidepoint(pygame.mouse.get_pos()):
                            pygame.draw.rect(screen, button_hover_color, ai_button2_rect)

                        if ai_button3_rect.collidepoint(pygame.mouse.get_pos()):
                            pygame.draw.rect(screen, button_hover_color, ai_button3_rect)

                        if ai_button4_rect.collidepoint(pygame.mouse.get_pos()):
                            pygame.draw.rect(screen, button_hover_color, ai_button4_rect)

                        screen.blit(ai_button1, ai_button1_rect)
                        screen.blit(ai_button2, ai_button2_rect)
                        screen.blit(ai_button3, ai_button3_rect)
                        screen.blit(ai_button4, ai_button4_rect)

                        pygame.display.flip()

                        clock.tick(60)

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                ai_menu_running = False

                            if event.type == pygame.MOUSEBUTTONDOWN:
                                mouse_pos = pygame.mouse.get_pos()

                                if ai_button1_rect.collidepoint(mouse_pos):
                                    board = Board(4, 4, screen, "bfs")
                                    board.run()

                                if ai_button2_rect.collidepoint(mouse_pos):
                                    board = Board(4, 4, screen, "minimax")
                                    board.run()

                                if ai_button3_rect.collidepoint(mouse_pos):
                                    board = Board(4, 4, screen, "iterative_deepening")
                                    board.run()

                                if ai_button4_rect.collidepoint(mouse_pos):
                                    board = Board(4, 4, screen, "a_star")
                                    board.run()


            if button3_rect.collidepoint(mouse_pos):
                print("Option 3 clicked!")
