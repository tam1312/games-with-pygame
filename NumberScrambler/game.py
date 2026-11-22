import pygame


pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()

pygame.display.set_caption("Number Scrambler!")
BACKGROUND_COLOR = "#FFB521"
RED = (255, 0, 0)
WHITE = (255, 255, 255)
FPS = 60

instruction_font = pygame.font.Font(None, 60)
instruction_text = instruction_font.render("Unscramble the word!", True, (0, 0, 0))
instruction_text_rect = instruction_text.get_rect(center=(WIDTH//2, HEIGHT//4))


def main():

    running = True

    #exit button
    exit_size = 70
    margin = 20
    exit_rect = pygame.Rect(
        WIDTH - exit_size - margin,
        margin,
        exit_size,
        exit_size
    )
    

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_rect.collidepoint(event.pos):
                    running = False


        screen.fill(BACKGROUND_COLOR)

        #exit button
        pygame.draw.rect(screen, RED, exit_rect, border_radius=8)

        #exit button X sign        
        pygame.draw.line(
            screen, WHITE,
            (exit_rect.left + 12, exit_rect.top + 12),
            (exit_rect.right - 12, exit_rect.bottom - 12), 6
        )

        pygame.draw.line(
            screen, WHITE,
            (exit_rect.right - 12, exit_rect.top + 12),
            (exit_rect.left + 12, exit_rect.bottom - 12), 6
        )

        #Instruction text
        screen.blit(instruction_text, instruction_text_rect)

        pygame.display.update()     


    pygame.quit()


if __name__ == "__main__":
    main()