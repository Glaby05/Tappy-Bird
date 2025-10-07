import pygame, Objects, random
from pygame.sprite import Sprite
from pygame.time import get_ticks
from pygame.mask import from_surface
import random

pygame.init()

screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h
FPS = 60
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tappy Bird")

COOLDOWN = random.randint(1000, 3000)
LAST_ACTION = 0

BG_IMAGE = pygame.image.load("assets/background.png").convert()
BG_IMAGE = pygame.transform.scale(BG_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))
ICE_BLOCK = pygame.image.load("assets/iceblock.png").convert_alpha()
STAR = pygame.image.load("assets/star.png").convert_alpha()

# Set the font for the start and game over screens
font = pygame.font.Font(None, 32)
big_font = pygame.font.Font(None, 48)

clock = pygame.time.Clock()

def get_scale_factor():
    """Calculate consistent scaling factor for all game elements"""
    width_scale = SCREEN_WIDTH / 1920  # 1920 is reference width
    height_scale = SCREEN_HEIGHT / 1080  # 1080 is reference height
    return min(width_scale, height_scale)  # Use smaller to maintain aspect ratio

class Level:
    """Holds and updates/draws all platform sprites."""
    def __init__(self):
        self.obstacle_list = pygame.sprite.Group()
        self.star_list = pygame.sprite.Group()

    def update(self):
        self.obstacle_list.update()
        self.star_list.update()

    def draw(self, surf, camera_x=0):
        # Clear background and draw all platforms with camera offset.
        bg_width = BG_IMAGE.get_width()
        start_x = -(camera_x % bg_width)

        # Draw enough copies to fill the whole screen
        for i in range(-1, SCREEN_WIDTH // bg_width + 2):
            surf.blit(BG_IMAGE, (start_x + i * bg_width, 0))

        for spr in self.obstacle_list:
            surf.blit(spr.image, (spr.rect.x - camera_x, spr.rect.y))

        for spr in self.star_list:
            surf.blit(spr.image, (spr.rect.x - camera_x, spr.rect.y))

def spawn_pair(camera_x):
    # Use consistent scaling factor
    scale_factor = get_scale_factor()
    
    # Calculate scaled obstacle dimensions
    scaled_ice_width = int(ICE_BLOCK.get_width() * scale_factor)
    scaled_ice_height = int(ICE_BLOCK.get_height() * scale_factor)
    
    # Ensure obstacles don't overlap with player's starting area
    spawn_x = camera_x + SCREEN_WIDTH + 50  # Spawn beyond screen edge
    
    # Create gap in the middle for player to pass through
    # Scale gap size based on screen size
    gap_size = int(300 * scale_factor)
    gap_center = SCREEN_HEIGHT // 2
    
    top_pos = (spawn_x, gap_center - gap_size // 2 - scaled_ice_height)
    bottom_pos = (spawn_x, gap_center + gap_size // 2)

    top_obstacle = Objects.Obstacle(top_pos)
    bottom_obstacle = Objects.Obstacle(bottom_pos)
    return top_obstacle, bottom_obstacle

def spawn_one(camera_x):
    placement = ["top", "bottom"]
    choice = random.choice(placement)

    # Use consistent scaling factor
    scale_factor = get_scale_factor()
    
    # Calculate scaled obstacle dimensions
    scaled_ice_width = int(ICE_BLOCK.get_width() * scale_factor)
    scaled_ice_height = int(ICE_BLOCK.get_height() * scale_factor)
    
    # Ensure obstacles don't overlap with player's starting area
    spawn_x = camera_x + SCREEN_WIDTH + 50  # Spawn beyond screen edge

    if choice == "top":
        top_pos = (spawn_x, 0)
        top_obstacle = Objects.Obstacle(top_pos)
        return top_obstacle
    else:
        bottom_pos = (spawn_x, SCREEN_HEIGHT - scaled_ice_height)
        bottom_obstacle = Objects.Obstacle(bottom_pos)
        return bottom_obstacle

def main():
    global LAST_ACTION
    level = Level()
    last_spawn = 0
    last_star_spawn = 0

    scale_factor = get_scale_factor()

    # Stamina bars
    full_stamina = pygame.image.load("assets/stamina_9-10.png").convert_alpha()
    fs_w, fs_h = int(full_stamina.get_width() * scale_factor * 1.2), int(full_stamina.get_height() * scale_factor * 1.2)
    scaled_fs = pygame.transform.scale(full_stamina, (fs_w, fs_h))

    se_stamina = pygame.image.load("assets/stamina_7-8.png").convert_alpha()
    se_w, se_h = int(se_stamina.get_width() * scale_factor * 1.2), int(se_stamina.get_height() * scale_factor * 1.2)
    scaled_se = pygame.transform.scale(se_stamina, (se_w, se_h))

    fs_stamina = pygame.image.load("assets/stamina_5-6.png").convert_alpha()
    fss_w, fss_h = int(fs_stamina.get_width() * scale_factor * 1.2), int(fs_stamina.get_height() * scale_factor * 1.2)
    scaled_fss = pygame.transform.scale(fs_stamina, (fss_w, fss_h))
    
    tf_stamina = pygame.image.load("assets/stamina_3-4.png").convert_alpha()
    tf_w, tf_h = int(tf_stamina.get_width() * scale_factor * 1.2), int(tf_stamina.get_height() * scale_factor * 1.2)
    scaled_tf = pygame.transform.scale(tf_stamina, (tf_w, tf_h))
    
    ot_stamina = pygame.image.load("assets/stamina_1-2.png").convert_alpha()
    ot_w, ot_h = int(ot_stamina.get_width() * scale_factor * 1.2), int(ot_stamina.get_height() * scale_factor * 1.2)
    scaled_ot = pygame.transform.scale(ot_stamina, (ot_w, ot_h))

    player = Objects.Player((SCREEN_WIDTH/3,SCREEN_HEIGHT/2))

    start = False
    game_over = False
    placement = ["pair", "single"]

    camera_x = 0.0
    SCROLL_TRIGGER = SCREEN_WIDTH * 0.6  # start scrolling when player passes 60% of screen
    # TODO: make the SCROLL_TRIGGER a variable that will be increased according to the level, 
    
    obstacles_group = pygame.sprite.Group() # TODO: issue -> why do we have obst_group and level.octs_list??
    player_group = pygame.sprite.Group()
    player_group.add(player)
    stars_group = pygame.sprite.Group()

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = True
                    # Only reduce stamina on key press, not continuous hold
                    if player.stamina > 0:
                        player.stamina -= 1
                        # player.rect -= 16
                        player.vel_y = player.jump_force
                        player.state = "jump"
                        player.jump_count += 1
                        # increase speed (difficulty) every 10 jumps
                        if player.jump_count % 50 == 0:  
                            player.speed += 1
                            for obs in obstacles_group:
                                obs.speed += 1
                            for star in stars_group:
                                star.speed += 1
                if event.key == pygame.K_r and game_over == True:
                    return main()
            if event.type == pygame.KEYUP:      
                if event.key == pygame.K_SPACE:
                    player.state = "idle"

        current_time = pygame.time.get_ticks()
        # if current_time - LAST_ACTION > COOLDOWN:
        if current_time - last_spawn > COOLDOWN:
            # obstacle
            choice = random.choice(placement)
            if choice == "pair":
                top, bottom = spawn_pair(camera_x)
                obstacles_group.add(top, bottom)
            else:
                block = spawn_one(camera_x)
                obstacles_group.add(block)
            last_spawn = current_time

        # if current_time - last_star_spawn > 500:
            # star
        if random.randint(0, 50) == 1:  # 1 in 200 chance per frame (once every few seconds)
            star = Objects.Star()
            spawn_x = SCREEN_WIDTH + 50  # just off right side
            max_attempts = 50
            safe = False
            for _ in range(max_attempts):
                # start slightly off-screen to the right
                star.rect.x = SCREEN_WIDTH + random.randint(50, 200)
                star.rect.y = random.randint(100, max(150, SCREEN_HEIGHT - 150))

                # check overlap with obstacles
                if not any(star.rect.colliderect(ob.rect.inflate(60, 60)) for ob in obstacles_group):
                    safe = True
                    break
            if not safe:
                star.rect.x = spawn_x + 100
                star.rect.y = random.randint(100, SCREEN_HEIGHT // 2)
            stars_group.add(star)
            print(f"star")
        last_star_spawn = current_time

            # LAST_ACTION = current_time

        if player.rect.top <= 0:
            player.rect.top = 0
        elif player.rect.bottom >= SCREEN_HEIGHT:
            player.rect.bottom = SCREEN_HEIGHT

        # Collision detection with obstacles
        for block in obstacles_group:
            if player.rect.colliderect(block.rect):  # quick AABB test
                offset_x = block.rect.left - player.rect.left
                offset_y = block.rect.top - player.rect.top
                if player.mask.overlap(block.mask, (offset_x, offset_y)):
                        game_over = True

        # Star collision
        for star in stars_group:
            if player.rect.colliderect(star.rect):
                offset_x = star.rect.left - player.rect.left
                offset_y = star.rect.top - player.rect.top
                if player.mask.overlap(star.mask, (offset_x, offset_y)):
                    # Restore some stamina
                    player.stamina = min(player.stamina + 5, 20)
                    star.kill()


        # --- Camera follow (only when player passes the trigger position) ---
        if player.rect.centerx > camera_x + SCROLL_TRIGGER:
            camera_x = player.rect.centerx - SCROLL_TRIGGER

        # Draw game elements
        if not game_over:
            level.draw(screen, camera_x)
            # obstacles_group.draw(screen)
            for block in obstacles_group:
                screen.blit(block.image, (block.rect.x - camera_x, block.rect.y))
            # draw stars
            for star in stars_group:
                screen.blit(star.image, (star.rect.x - camera_x, star.rect.y))
            # draw player
            screen.blit(player.image, (player.rect.x - camera_x, player.rect.y))

        # Handle game states
        if start == False:
            # Show start screen
            go = big_font.render("Start Game  —  Press SPACE to Start", True, (255, 80, 80))
            screen.blit(go, (SCREEN_WIDTH // 2 - go.get_width() // 2, SCREEN_HEIGHT // 2 - go.get_height() // 2))
        elif not game_over:
            # Update game objects only if game is not over
            obstacles_group.update()
            player_group.update()
            stars_group.update()

        if 17 <= player.stamina <= 20:
            screen.blit(scaled_fs, (50,50))
        elif 13 <= player.stamina <= 16:
            screen.blit(scaled_se, (50,50))
        elif 9 <= player.stamina <= 12:
            screen.blit(scaled_fss, (50,50))
        elif 5 <= player.stamina <= 8:
            screen.blit(scaled_tf, (50,50))
        elif 1 <= player.stamina <= 4:
            screen.blit(scaled_ot, (50,50))
        elif player.stamina <= 0:
            game_over = True

        if game_over:
            # Show game over message
            end = big_font.render("GAME OVER  —  Press R to Restart", True, (255, 80, 80))
            screen.blit(end, (SCREEN_WIDTH // 2 - end.get_width() // 2, SCREEN_HEIGHT // 2 - end.get_height() // 2))

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()