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
    pass


class PowerUp(pygame.sprite.Sprite):
    pass

