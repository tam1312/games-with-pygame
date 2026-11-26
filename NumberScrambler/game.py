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
YELLOW = (255, 255, 0)

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

numbers_audio = {
    11: "audio/eleven.mp3",
    12: "audio/twelve.mp3", 
    13: "audio/thirteen.mp3",
    14: "audio/fourteen.mp3",
    15: "audio/fifteen.mp3",
    16: "audio/sixteen.mp3",
    17: "audio/seventeen.mp3",
    18: "audio/eighteen.mp3",
    19: "audio/nineteen.mp3",
    20: "audio/twenty.mp3"
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

    game_sound = pygame.mixer.Sound(numbers_audio[game_number])
    number_spoken = False

    yay_sound = pygame.mixer.Sound("audio/yay-kids.mp3")
    yay_sound_played = False
    yay_sound_timer_start = 0

    correct_order = list(game_word)
    scrambled_order = correct_order.copy()
    random.shuffle(scrambled_order)

    BOXSIZE = 130

    selected_scrambled_rect = None
    selected_ordered_rect = None

    highlight_start_time = None
    HIGHLIGHT_DURATION = 1000

    answer_list = [None] * len(correct_order) #ex. eleven => [None, None, None, None, None, None]
    used_letters = [False] * len(scrambled_order) #helps with not removing duplicate letters
    
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

                    correct_order = list(game_word)
                    scrambled_order = correct_order.copy()
                    random.shuffle(scrambled_order)

                    selected_scrambled_rect = None
                    selected_ordered_rect = None

                    answer_list = [None] * len(correct_order)
                    used_letters = [False] * len(scrambled_order)

                    game_sound = pygame.mixer.Sound(numbers_audio[game_number])
                    number_spoken = False
                    yay_sound_played = False
                    yay_sound_timer_start = 0


                    hint_visible = False
                for i, rect in enumerate(scrambled_rects):
                    if rect.collidepoint(event.pos):
                        if selected_scrambled_rect == i:
                            selected_scrambled_rect = None
                        else:
                            selected_scrambled_rect = i

                for i, rect in enumerate(ordered_rects):
                    if rect.collidepoint(event.pos):
                        if selected_ordered_rect == i:
                            selected_ordered_rect = None
                        else:
                            selected_ordered_rect = i
                if selected_ordered_rect is not None and selected_scrambled_rect is not None:
                    valid = check_boxes(selected_scrambled_rect, selected_ordered_rect,
                                correct_order, scrambled_order, answer_list, used_letters)
                    if valid:
                        highlight_start_time = pygame.time.get_ticks()

                    else:
                        selected_scrambled_rect = None
                        selected_ordered_rect = None

        if highlight_start_time is not None:
            current_time = pygame.time.get_ticks()
            if current_time - highlight_start_time >= HIGHLIGHT_DURATION:
                selected_scrambled_rect = None
                selected_ordered_rect = None
                highlight_start_time = None

        #if the word has been unscrambled
        if False not in used_letters and not number_spoken: 
            hint_visible = True
            game_sound.play()
            number_spoken = True

            yay_sound_timer_start = pygame.time.get_ticks()

            #play yay after 2 seconds
        if number_spoken and not yay_sound_played:
            current_time = pygame.time.get_ticks()

            if current_time - yay_sound_timer_start >= 1500:
                yay_sound.play()
                yay_sound_played = True


        screen.fill(BACKGROUND_COLOR)
        scrambled_rects = draw_scrambled_word(scrambled_order, BOXSIZE, margin, used_letters)
        ordered_rects = draw_correct_word(answer_list, BOXSIZE, margin)

        #draw a border around the selected scrambled rect
        if selected_scrambled_rect is not None:
            draw_border(scrambled_rects[selected_scrambled_rect])

        #draw a border around the selected ordered rect
        if selected_ordered_rect is not None:
            draw_border(ordered_rects[selected_ordered_rect])

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


def draw_scrambled_word(mixed_order, BOXSIZE, margin, used_letters):
    # ex. seventeen: 9 * 90 + 8 * 20 = 970 (9 * BOXSIZE + 8 * margin)
    num_letters = len(mixed_order)
    total_width = (num_letters * BOXSIZE) + ((num_letters - 1) * margin)

    start_x = (WIDTH - total_width) // 2

    #new list for the rectangles to keep track of them
    scrambled_rects = []

    for i, letter in enumerate(mixed_order):
        x = start_x + i * (BOXSIZE + margin)
        y = HEIGHT // 3 * 2
        
        rect = pygame.Rect(x, y, BOXSIZE, BOXSIZE)
        pygame.draw.rect(screen, GRAY, rect, border_radius=8)

        scrambled_rects.append(rect)

        '''if mixed_order[i] not in answer_list:
            #draw a letter in the box if it's not been solved 
            letter_text = letter_font.render(letter, True, BLACK)
            letter_text_rect = letter_text.get_rect(center=rect.center)

            screen.blit(letter_text, letter_text_rect)'''

        if not used_letters[i]:
            letter_text = letter_font.render(letter, True, BLACK)
            letter_text_rect = letter_text.get_rect(center=rect.center)

            screen.blit(letter_text, letter_text_rect)

    return scrambled_rects


def draw_correct_word(answer_list, BOXSIZE, margin):
    num_letters = len(answer_list)
    total_width = (num_letters * BOXSIZE) + ((num_letters - 1) * margin)

    start_x = (WIDTH - total_width) // 2

    #list of the rectangles to keep track of
    ordered_rects = []

    for i, letter in enumerate(answer_list):
        x = start_x + i * (BOXSIZE + margin)
        y = HEIGHT // 3 + (HEIGHT // 3) // 3
        
        rect = pygame.Rect(x, y, BOXSIZE, BOXSIZE)
        pygame.draw.rect(screen, WHITE, rect, border_radius=8)

        ordered_rects.append(rect)

        #draw the letter if the slot is occupied
        if letter is not None:

            letter_text = letter_font.render(letter, True, BLACK)
            letter_text_rect = letter_text.get_rect(center=rect.center)

            screen.blit(letter_text, letter_text_rect)


    return ordered_rects


def draw_border(rect):
    pygame.draw.rect(screen, YELLOW, rect, 10, border_radius=8)


def check_boxes(scrambled_index, ordered_index, 
                correct_order, scrambled_order, answer_list, used_letters):
    
    scrambled_letter = scrambled_order[scrambled_index]
    correct_letter = correct_order[ordered_index]

    if scrambled_letter == correct_letter:
        print("Correct!")
        answer_list[ordered_index] = scrambled_letter
        used_letters[scrambled_index] = True

        return True

    return False


if __name__ == "__main__":
    main()