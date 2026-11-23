import pygame
import random


pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()

pygame.display.set_caption("Number Scrambler!")
BACKGROUND_COLOR = "#FFB521"
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = "#E5E4E2"

FPS = 60

numbers = {
    11: "ELEVEN",
    12: "TWELVE", 
    13: "THIRTEEN",
    14: "FOURTEEN",
    15: "FIFTEEN",
    16: "SIXTEEN",
    17: "SEVENTEEN",
    18: "EIGHTEEN",
    19: "NINETEEN",
    20: "TWENTY"
}


#instruction text
instruction_font = pygame.font.Font(None, 60)
instruction_text = instruction_font.render("Unscramble the word!", True, BLACK)
instruction_text_rect = instruction_text.get_rect(center=(WIDTH//2, HEIGHT//4))

#scrambled word text
letter_font = pygame.font.Font(None, 70)


def main():

    running = True

    hint_visible = False

    game_number = random.randint(11,20)
    game_word = numbers[game_number]

    correct_order = list(game_word)
    mixed_order = correct_order.copy()
    random.shuffle(mixed_order)

    BOXSIZE = 130

    
    #exit button
    exit_size = 70
    margin = 20
    exit_rect = pygame.Rect(
        WIDTH - exit_size - margin,
        margin,
        exit_size,
        exit_size
    )

    #hint button
    hint_img = pygame.image.load('images/lightbulb.png').convert_alpha()
    hint_rect = hint_img.get_rect(topleft=(margin + 5, margin + 5))

    #change button
    change_img = pygame.image.load('images/change.png').convert_alpha()
    change_rect = change_img.get_rect(topleft=(margin, margin * 7))

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_rect.collidepoint(event.pos):
                    running = False
                if hint_rect.collidepoint(event.pos):
                    hint_visible = False if hint_visible else True
                if change_rect.collidepoint(event.pos):
                    game_number = random.randrange(11,20)
                    game_word = numbers[game_number]
                

        screen.fill(BACKGROUND_COLOR)
        draw_scrambled_word(mixed_order, BOXSIZE, margin)

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

        #hint button
        screen.blit(hint_img, hint_rect)

        #change button
        screen.blit(change_img, change_rect)

        if hint_visible:
            hint_button(game_number)

        pygame.display.update()     


    pygame.quit()


def hint_button(number):
    #print(f"Clicked on hint!! Your number is: {number}")
    
    hint_font = pygame.font.Font(None, 150)
    hint_text = hint_font.render(f"{number}", True, (0, 0, 0))
    hint_text_rect = hint_text.get_rect(center=(WIDTH//2, HEIGHT//6))

    screen.blit(hint_text, hint_text_rect)
    pygame.display.update()


def draw_scrambled_word(mixed_order, BOXSIZE, margin):
    # ex. seventeen: 9 * 90 + 8 * 20 = 970 (9 * BOXSIZE + 8 * margin)
    num_letters = len(mixed_order)
    total_width = (num_letters * BOXSIZE) + ((num_letters - 1) * margin)

    start_x = (WIDTH - total_width) // 2

    for i, letter in enumerate(mixed_order):
        x = start_x + i * (BOXSIZE + margin)
        y = HEIGHT // 3 * 2
        
        rect = pygame.Rect(x, y, BOXSIZE, BOXSIZE)
        pygame.draw.rect(screen, GRAY, rect)

        #draw a letter in the box
        letter_text = letter_font.render(letter, True, BLACK)
        letter_text_rect = letter_text.get_rect(center=rect.center)

        screen.blit(letter_text, letter_text_rect)
        
    
if __name__ == "__main__":
    main()