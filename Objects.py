import pygame, TappyBirdMain, random
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

        # Player frames
        self.fall = pygame.image.load("assets/fall.png").convert_alpha()
        self.jump = pygame.image.load("assets/jump.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        # Motion parameters
        # self.speed = 5
        self.gravity = 1 # The speed of which the bird falls

        # Player attributes
        self.state = "idle"
        self.stamina = 20

        self.mask = from_surface(self.image)

    # Physics and input
    def update(self):
        # Horizontal movement (constant forward movement)
        self.rect.x += 5
        
        # Apply gravity
        self.rect.y += self.gravity
        
        # Handle jumping (stamina consumption moved to main loop for tap-based input)
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.stamina > 0:
            self.state = "jump"
            self.image = self.jump
            self.rect.y -= 16  # Jump force
        else:
            self.state = "idle"
            self.image = self.fall

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
        self.speed = 5

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
        self.image = pygame.image.load("assets/star.png").convert_alpha()
        self.rect = self.image.get_rect()

        #TODO: add random position when initializing the star
        # self.rect.center = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) 

    def update(self):
        """
        At star_group (the sprite group for stars) -> remove the star when it collides with the player 
        && also when the star reaches the left edge of the screen.
        """
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
        """Decrease life by n every second. (by doing self.rect.x - n) 
        ^^^rendering the life bar image every stage of life span
        """
        pass



