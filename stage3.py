import pygame
import sys

def show_team_a():
    pygame.init()

    # Set the display dimensions
    width, height = 400, 200
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Team A")

    # Set up fonts
    font = pygame.font.SysFont(None, 120)  # Default system font with size 48

    # Set up colors
    black = (0, 0, 0)
    white = (255, 255, 255)

    # Create text surface
    text_surface = font.render("TEAM A", True, white)

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the screen with black
        screen.fill(black)

        # Center the text on the screen
        text_rect = text_surface.get_rect(center=(width // 2, height // 2))

        # Blit the text onto the screen
        screen.blit(text_surface, text_rect)

        # Update the display
        pygame.display.flip()

    pygame.quit()

# Call the function to display "TEAM A"
#show_team_a()
