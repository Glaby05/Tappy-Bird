import pygame, TappyBirdMain, random
from pygame.time import get_ticks
from pygame.mask import from_surface
import math

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

        # Player frames
        # self.fall = pygame.image.load("assets/fall.png").convert_alpha()
        # self.jump = pygame.image.load("assets/jump.png").convert_alpha()

        fall = pygame.image.load("assets/fall.png").convert_alpha()
        jump = pygame.image.load("assets/jump.png").convert_alpha()
        scale_factor = TappyBirdMain.get_scale_factor()
        self.fall = (int(fall.get_width() * scale_factor * 1.2), int(fall.get_height() * scale_factor))
        self.jump = (int(jump.get_width() * scale_factor * 1.2), int(jump.get_height() * scale_factor))

        self.rect = self.image.get_rect(topleft=pos)

        # Motion parameters
        # self.speed = 5
        self.gravity = 2 # The speed of which the bird falls

        # Player attributes
        self.state = "idle"
        self.stamina = 20

        self.mask = from_surface(self.image)

    # Physics and input
    def update(self):
        # Horizontal movement (constant forward movement)
        self.rect.x += 3
        
        # Apply gravity
        self.rect.y += self.gravity
        
        # Handle jumping (stamina consumption moved to main loop for tap-based input)
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.stamina > 0:
            self.state = "jump"
            # self.image = self.jump
            self.image = pygame.transform.scale(self.image, (self.jump[0], self.jump[1]))
            self.rect.y -= 16  # Jump force
        else:
            self.state = "idle"
            # self.image = self.fall
            self.image = pygame.transform.scale(self.image, (self.fall[0], self.fall[1]))

        self.mask = from_surface(self.image)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = TappyBirdMain.ICE_BLOCK
        
        # Use consistent scaling factor from main module
        scale_factor = TappyBirdMain.get_scale_factor()
        
        # Apply scaling
        scaled_width = int(self.image.get_width() * scale_factor)
        scaled_height = int(self.image.get_height() * scale_factor)
        self.image = pygame.transform.scale(self.image, (scaled_width, scaled_height))
        
        # Store the scale factor for collision detection
        self.scale_factor = scale_factor
        
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = 3

        self.mask = from_surface(self.image)

    def update(self):
        """load walls from image{random number}."""
        self.rect.x -= self.speed

        if self.rect.right < 0:
            self.kill()


class Star(pygame.sprite.Sprite):
    """objects that (dis-)appear in reaction to player activities.
    (when collided with player)"""
    def __init__(self):
        super().__init__()
        star = pygame.image.load("assets/star.png").convert_alpha()
        scale_factor = TappyBirdMain.get_scale_factor()
        star_width = int(star.get_width() * scale_factor * 0.4)
        star_height = int(star.get_height() * scale_factor * 0.4)

        self.image = pygame.transform.scale(star, (star_width, star_height))

        self.rect = self.image.get_rect()
        # Random position when initializing the star
        # self.rect.x = TappyBirdMain.SCREEN_WIDTH + random.randint(50, 200)
        # self.rect.y = random.randint(100, max(150, TappyBirdMain.SCREEN_HEIGHT - 150))

        self.speed = 3
        self.mask = from_surface(self.image)


    def update(self):
        """
        At star_group (the sprite group for stars) -> remove the star when it collides with the player 
        && also when the star reaches the left edge of the screen.
        """
        self.rect.x -= self.speed
        # gentle up-down motion
        self.rect.y += int(2 * math.sin(pygame.time.get_ticks() / 200)) 
        if self.rect.right < 0:
            self.kill()



