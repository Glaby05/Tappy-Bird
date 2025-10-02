import pygame
from pygame.time import get_ticks
from pygame.mask import from_surface

# appropriate scaling behaviour (e.g. another level, a boss enemy)
# life decreases faster and player moves faster overtime

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, image=None):
        super().__init__()
        if image:
            self.image = pygame.image.load(image).convert_alpha()
        else:
            self.image = pygame.Surface((64, 64), pygame.SRCALPHA)

        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Player(Sprite):
    """objects that move over time.
    objects who move or are transformed in reaction to user activities."""
    def __init__(self, pos):
        super().__init__(pos, "assets/fall.png")

        #Animation frames
        self.fall = pygame.image.load("assets/fall.png").convert_alpha()
        self.jump = pygame.image.load("assets/jump.png").convert_alpha()

        self.rect = self.image.get_rect(topleft=pos)

        self.state = "idle"

    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            self.state = "jump"
            self.image = self.jump
        else:
            self.state = "idle"
            self.image = self.fall



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

