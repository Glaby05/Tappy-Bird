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


if __name__ == '__main__':
    g = Game()
    print("starting...")
    g.run()
    print("shuting down...")
    pygame.quit()

