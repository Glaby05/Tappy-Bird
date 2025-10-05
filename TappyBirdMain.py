import pygame, Objects, random
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

COOLDOWN = 3000
LAST_ACTION = 0

BG_IMAGE = pygame.image.load("assets/background.png").convert()
BG_IMAGE = pygame.transform.scale(BG_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))
ICE_BLOCK = pygame.image.load("assets/iceblock.png").convert_alpha()

# Set the font for the start and game over screens
font = pygame.font.Font(None, 32)
big_font = pygame.font.Font(None, 48)

clock = pygame.time.Clock()

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

def spawn_pair():
    top_pos = (SCREEN_WIDTH, -40)
    bottom_pos = (SCREEN_WIDTH, SCREEN_HEIGHT - ICE_BLOCK.get_height() + 60)

    top_obstacle = Objects.Obstacle(top_pos)
    bottom_obstacle = Objects.Obstacle(bottom_pos)
    return top_obstacle, bottom_obstacle

def spawn_one():
    placement = ["top", "bottom"]
    choice = random.choice(placement)

    if choice == "top":
        top_pos = (SCREEN_WIDTH, 0)
        top_obstacle = Objects.Obstacle(top_pos)
        return top_obstacle
    else:
        bottom_pos = (SCREEN_WIDTH, SCREEN_HEIGHT - ICE_BLOCK.get_height())
        bottom_obstacle = Objects.Obstacle(bottom_pos)
        return bottom_obstacle

def main():
    global LAST_ACTION
    level = Level()

    # Stamina bars
    full_stamina = pygame.image.load("assets/stamina_9-10.png")
    se_stamina = pygame.image.load("assets/stamina_7-8.png")
    fs_stamina = pygame.image.load("assets/stamina_5-6.png")
    tf_stamina = pygame.image.load("assets/stamina_3-4.png")
    ot_stamina = pygame.image.load("assets/stamina_1-2.png")

    player = Objects.Player((SCREEN_WIDTH/3,SCREEN_HEIGHT/2))

    start = False
    game_over = False
    placement = ["pair", "single"]

    camera_x = 0.0
    SCROLL_TRIGGER = SCREEN_WIDTH * 0.6  # start scrolling when player passes 60% of screen

    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    player_group.add(player)

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
                if event.key == pygame.K_r and game_over == True:
                    main()

        current_time = pygame.time.get_ticks()
        if current_time - LAST_ACTION > COOLDOWN:
            choice = random.choice(placement)
            if choice == "pair":
                top, bottom = spawn_pair()
                all_sprites.add(top, bottom)
            else:
                block = spawn_one()
                all_sprites.add(block)
            LAST_ACTION = current_time

        if player.rect.top <= 0:
            player.rect.top = 0
        elif player.rect.bottom >= SCREEN_HEIGHT:
            player.rect.bottom = SCREEN_HEIGHT

        # --- Camera follow (only when player passes the trigger position) ---
        if player.rect.centerx > camera_x + SCROLL_TRIGGER:
            camera_x = player.rect.centerx - SCROLL_TRIGGER

        if not game_over:
            level.draw(screen, camera_x)
            all_sprites.draw(screen)
            screen.blit(player.image, (player.rect.x - camera_x, player.rect.y))

        if start == False:
            go = big_font.render("Start Game  —  Press SPACE to Start", True, (255, 80, 80))
            screen.blit(go, (SCREEN_WIDTH // 2 - go.get_width() // 2, SCREEN_HEIGHT // 2 - go.get_height() // 2))
        else:
            all_sprites.update()
            player_group.update()

        if 17 <= player.stamina <= 20:
            screen.blit(full_stamina, (50,50))
        elif 13 <= player.stamina <= 16:
            screen.blit(se_stamina, (50,50))
        elif 9 <= player.stamina <= 12:
            screen.blit(fs_stamina, (50,50))
        elif 5 <= player.stamina <= 8:
            screen.blit(tf_stamina, (50,50))
        elif 1 <= player.stamina <= 4:
            screen.blit(ot_stamina, (50,50))
        elif player.stamina <= 0:
            game_over = True

        if game_over:
            end = big_font.render("GAME OVER  —  Press R to Restart", True, (255, 80, 80))
            screen.blit(end, (SCREEN_WIDTH // 2 - end.get_width() // 2, SCREEN_HEIGHT // 2 - end.get_height() // 2))

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()

