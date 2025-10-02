import pygame
from pygame.time import get_ticks
from pygame.mask import from_surface

class Game:
    """ This class represents the Game. It contains all the game objects. """
    def __init__(self):
        pass

    def poll(self):
        """mouse/keyboard event handler."""
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def run(self):
        pass

def main():
    pygame.init()
    screen_info = pygame.display.Info()
    SCREEN_WIDTH = screen_info.current_w
    SCREEN_HEIGHT = screen_info.current_h
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Set the font for the start and game over screens
    font = pygame.font.Font(None, 32)
    big_font = pygame.font.Font(None, 48)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    # g = Game()
    # print("starting...")
    # g.run()
    # print("shutting down...")
    # pygame.quit()
    main()

