import pygame, Objects
from pygame.sprite import Sprite
from pygame.time import get_ticks
from pygame.mask import from_surface

pygame.init()

screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h
FPS = 60
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tappy Bird")

BG_IMAGE = pygame.image.load("assets/background.png").convert()
BG_IMAGE = pygame.transform.scale(BG_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

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

class Level:
    """Holds and updates/draws all platform sprites."""
    def __init__(self):
        self.obstacle_list = pygame.sprite.Group()

    def update(self):
        self.obstacle_list.update()

    def draw(self, surf, camera_x=0):
        # Clear background and draw all platforms with camera offset.
        bg_width = BG_IMAGE.get_width()
        start_x = -(camera_x % bg_width)

        # Draw enough copies to fill the whole screen
        for i in range(-1, SCREEN_WIDTH // bg_width + 2):
            surf.blit(BG_IMAGE, (start_x + i * bg_width, 0))

        for spr in self.obstacle_list:
            surf.blit(spr.image, (spr.rect.x - camera_x, spr.rect.y))

class LevelLab4(Level):
    """
    Ground row + three island rows + a moving platform.
    Supports chunk-based extension to the right.
    """
    def __init__(self):
        super().__init__()
        self.row_gap = 150
        self.right_edge = 0
        self.build_initial()

    def build_initial(self):
        """Build the first screen of tiles."""
        self.build_chunk(0, SCREEN_WIDTH)
        self.right_edge = SCREEN_WIDTH

    def build_chunk(self, start_x, end_x):
        """Build terrain in [start_x, end_x)."""
        pass

def main():
    level = LevelLab4()

    # Stamina bars
    full_stamina = pygame.image.load("assets/stamina_9-10.png")
    se_stamina = pygame.image.load("assets/stamina_7-8.png")
    fs_stamina = pygame.image.load("assets/stamina_5-6.png")
    tf_stamina = pygame.image.load("assets/stamina_3-4.png")
    ot_stamina = pygame.image.load("assets/stamina_1-2.png")

    # Set the font for the start and game over screens
    font = pygame.font.Font(None, 32)
    big_font = pygame.font.Font(None, 48)

    player = Objects.Player(level, (SCREEN_WIDTH/3,SCREEN_HEIGHT/2))
    start = False

    camera_x = 0.0
    SCROLL_TRIGGER = SCREEN_WIDTH * 0.6  # start scrolling when player passes 60% of screen
    CHUNK_SIZE = 600                     # how much new terrain to add per extension

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = True
                    player.stamina -= 1

        # --- Camera follow (only when player passes the trigger position) ---
        if player.rect.centerx > camera_x + SCROLL_TRIGGER:
            camera_x = player.rect.centerx - SCROLL_TRIGGER

        # --- Extend level to the right on demand ---
        while level.right_edge < camera_x + SCREEN_WIDTH + 200:
            level.build_chunk(level.right_edge, level.right_edge + CHUNK_SIZE)
            level.right_edge += CHUNK_SIZE

        if start == False:
            go = big_font.render("Start Game  —  Press SPACE to Start", True, (255, 80, 80))
            screen.blit(go, (SCREEN_WIDTH // 2 - go.get_width() // 2, SCREEN_HEIGHT // 2 - go.get_height() // 2))
        else:
            all_sprites.update()

        level.draw(screen, camera_x)
        screen.blit(player.image, (player.rect.x - camera_x, player.rect.y))

        if 9 <= player.stamina <= 10:
            screen.blit(full_stamina, (50,50))
        elif 7 <= player.stamina <= 8:
            screen.blit(se_stamina, (50,50))
        elif 5 <= player.stamina <= 6:
            screen.blit(fs_stamina, (50,50))
        elif 3 <= player.stamina <= 4:
            screen.blit(tf_stamina, (50,50))
        elif 1 <= player.stamina <= 2:
            screen.blit(ot_stamina, (50,50))

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    # g = Game()
    # print("starting...")
    # g.run()
    # print("shutting down...")
    # pygame.quit()
    main()

