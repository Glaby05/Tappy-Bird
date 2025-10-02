import pygame
from pygame.time import get_ticks
from pygame.mask import from_surface

# appropriate scaling behaviour (e.g. another level, a boss enemy)
# life decreases faster and player moves faster overtime

def load_player_sheet(sheet, x, y, w, h):
    """Extract a sprite from the sheet at (x, y) with size (w, h)."""
    sprite = pygame.Surface((w, h), pygame.SRCALPHA)
    sprite.blit(sheet, (0, 0), (x, y, w, h))
    return sprite

sheet = pygame.image.load("assets/Flap.png").convert_alpha()
fall_img = load_player_sheet(sheet, 0, 0, 64, 64)
jump_img = load_player_sheet(sheet, 64, 0, 64, 64)

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
        super().__init__(fall_img, startx, starty)

    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            self.image = jump_img


class Wall(pygame.sprite.Sprite):
    """objects that (dis-)appear in reaction to player activities.
    (if shot when player powered up)"""
    def __init__(self):
        super().__init__()

        pass

    def update(self):
        """load walls from image{random number}."""
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

