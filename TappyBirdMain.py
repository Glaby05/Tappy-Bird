import pygame, Objects
from pygame.time import get_ticks
from pygame.mask import from_surface

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

def main():
    pygame.init()
    screen_info = pygame.display.Info()
    SCREEN_WIDTH = screen_info.current_w
    SCREEN_HEIGHT = screen_info.current_h
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    bg_image = pygame.image.load("assets/background.png").convert()
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Stamina bars
    full_stamina = pygame.image.load("assets/stamina_9-10.png")
    se_stamina = pygame.image.load("assets/stamina_7-8.png")
    fs_stamina = pygame.image.load("assets/stamina_5-6.png")
    tf_stamina = pygame.image.load("assets/stamina_3-4.png")
    ot_stamina = pygame.image.load("assets/stamina_1-2.png")

    # Set the font for the start and game over screens
    font = pygame.font.Font(None, 32)
    big_font = pygame.font.Font(None, 48)

    player = Objects.Player((SCREEN_WIDTH/3,SCREEN_HEIGHT/2))
    start = False

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = True
                    player.stamina -= 1

        screen.blit(bg_image, (0,0))
        player.draw(screen)

        if start == False:
            go = big_font.render("Start Game  —  Press SPACE to Start", True, (255, 80, 80))
            screen.blit(go, (SCREEN_WIDTH // 2 - go.get_width() // 2, SCREEN_HEIGHT // 2 - go.get_height() // 2))
        else:
            all_sprites.update()

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

