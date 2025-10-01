import pygame
from pygame.time import get_ticks
from pygame.mask import from_surface

# appropriate scaling behaviour (e.g. another level, a boss enemy)
# life decreases faster and player moves faster overtime
class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, startx, starty):
        super().__init__()

        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.center = [startx, starty]

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Player(Sprite):
    """objects that move over time.
    objects who move or are transformed in reaction to user activities."""
    def __init__(self, startx, starty, index=0):
        super().__init__("assets/Flap.png", startx, starty)

        tile_width = 64
        tile_height = 64

        x = tile_width * index
        rect = pygame.Rect(x, 0, tile_width, tile_height)

        self.image = self.image.subsurface(rect).copy()
        self.rect = self.image.get_rect(topleft=(startx, starty))


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

