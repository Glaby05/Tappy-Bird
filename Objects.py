import pygame
from pygame.time import get_ticks
from pygame.mask import from_surface

# appropriate scaling behaviour (e.g. another level, a boss enemy)
# life decreases faster and player moves faster overtime


class Player(pygame.sprite.Sprite):
    """objects that move over time.
    objects who move or are transformed in reaction to user activities."""
    pass


class Wall(pygame.sprite.Sprite):
    """objects that (dis-)appear in reaction to player activities.
    (if shot when player powered up)"""
    pass


class Star(pygame.sprite.Sprite):
    """objects that (dis-)appear in reaction to player activities.
    (when collided with player)"""
    pass


class Life(pygame.sprite.Sprite):
    """Objects who move or are transformed in reaction to user activities."""
    def __init__(self):
        super().__init__()

        # self.image = pygame.Surface([20, 15])
        self.image = pygame.Surface((100, 30))
        self.image.fill((253, 234, 14))  # or set_colorkey()
        self.rect = self.image.get_rect()
        # self.rect.left = SET THE LOCATION ACCORDING TO THE WINDOW

    def update(self):
        """Decrease life by n every second. (by doing self.rect.x - n) """
        pass


class PowerUp(pygame.sprite.Sprite):
    pass

