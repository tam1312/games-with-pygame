import pygame


pygame.display.set_caption("Number Scrambler!")
BACKGROUND_COLOR = "#FFB521"
FPS = 60


def main():

    pygame.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    WIDTH, HEIGHT = screen.get_size()

    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               running = False

        screen.fill(BACKGROUND_COLOR)
        
        pygame.display.update()     

    pygame.quit()


if __name__ == "__main__":
    main()