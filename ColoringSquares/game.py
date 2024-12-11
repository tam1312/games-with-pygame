import random

import pygame
pygame.init()

screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption('Game of Squares')
clock = pygame.time.Clock()

# colors
BLUE = '#ecfaff'
PEACH = '#fac5c6'
GREEN = '#96b783'
RED = '#f45f56'
PINK = '#e27fb4'
ORANGE = '#ff8b3b'

colors = [GREEN, RED, PINK, ORANGE]

# background
background_img = pygame.image.load('images/background/background.png').convert()


# text
test_font = pygame.font.Font('font/DancingScript.ttf', 40)

text_colors = test_font.render("Change colors!", True, 'hotpink')
text_colors_rect = text_colors.get_rect(topleft=(530, 50))

text_startAgain = test_font.render("START AGAIN", True, 'hotpink')
text_startAgain_rect = text_startAgain.get_rect(topleft=(520, 400))

test_font = pygame.font.Font('font/DancingScript.ttf', 100)
game_lost_text = test_font.render("GAME LOST", True, 'black')
game_lost_text_rect = game_lost_text.get_rect(topleft=(170, 150))

you_won_text = test_font.render("YOU WON", True, 'black')
you_won_text_rect = you_won_text.get_rect(topleft=(170, 150))

test_font = pygame.font.Font('font/DancingScript.ttf', 50)
restarting_in_text = test_font.render("Restarting in", True, 'black')
restarting_in_text_rect = restarting_in_text.get_rect(topleft=(270, 270))

countdown_text = test_font.render(" ", True, 'black')
countdown_text_rect = countdown_text.get_rect(topleft=(530, 265))
countdown_text_bg = pygame.Surface((50, 50)) #bg for the countdown number for game over screen
countdown_text_bg.fill(RED)

test_font = pygame.font.Font('font/DancingScript.ttf', 30)
computer_score_text = test_font.render("computer:", True, RED)
computer_score_text_rect = computer_score_text.get_rect(topleft=(100, 10))
computer_score_number = test_font.render("", True, RED)
computer_score_number_rect = computer_score_number.get_rect(topleft=(210, 10))

player_score_text = test_font.render("you:", True, RED)
player_score_text_rect = player_score_text.get_rect(topleft=(350, 10))
player_score_number = test_font.render("", True, RED)
player_score_number_rect = player_score_number.get_rect(topleft=(400, 10))



# buckets
red_bucket = pygame.image.load('images/buckets/red_bucket.png').convert_alpha()
red_bucket_rect = red_bucket.get_rect(topleft=(550, 110))
orange_bucket = pygame.image.load('images/buckets/orange_bucket.png').convert_alpha()
orange_bucket_rect = orange_bucket.get_rect(topleft=(650, 130))
pink_bucket = pygame.image.load('images/buckets/pink_bucket.png').convert_alpha()
pink_bucket_rect = pink_bucket.get_rect(topleft=(550, 220))
green_bucket = pygame.image.load('images/buckets/green_bucket.png').convert_alpha()
green_bucket_rect = green_bucket.get_rect(topleft=(650, 240))

# brushes
red_brush = pygame.image.load('images/brushes/red_brush1.png').convert_alpha()
orange_brush = pygame.image.load('images/brushes/orange_brush1.png').convert_alpha()
pink_brush = pygame.image.load('images/brushes/pink_brush1.png').convert_alpha()
green_brush = pygame.image.load('images/brushes/green_brush1.png').convert_alpha()
brush_size = (73, 100)
CURRENT_BRUSH = red_brush


# mouse
pygame.mouse.set_visible(False)

# grid square
XMARGIN = 70
YMARGIN = 50
GRID_SIZE = 400
NUM_CELLS = 5
BOXSIZE = GRID_SIZE // NUM_CELLS
GAPSIZE = 2

grid_colors = [[PEACH for _ in range(NUM_CELLS)] for _ in range(NUM_CELLS)]

COLOR_OF_BOX = RED

game_lost = False
start_timer = 0

player_turn = True
computer_points = 0
player_points = 0

def main():
    global CURRENT_BRUSH, COLOR_OF_BOX
    mouseClicked = False
    global game_lost, start_timer
    global player_turn
    global computer_points, player_points


    while True:
        mousex, mousey = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()



            if event.type == pygame.MOUSEBUTTONDOWN:
                global CURRENT_BRUSH, COLOR_OF_BOX
                if red_bucket_rect.collidepoint(event.pos):
                    CURRENT_BRUSH = red_brush
                    COLOR_OF_BOX = RED
                elif orange_bucket_rect.collidepoint(event.pos):
                    CURRENT_BRUSH = orange_brush
                    COLOR_OF_BOX = ORANGE
                elif pink_bucket_rect.collidepoint(event.pos):
                    CURRENT_BRUSH = pink_brush
                    COLOR_OF_BOX = PINK
                elif green_bucket_rect.collidepoint(event.pos):
                    CURRENT_BRUSH = green_brush
                    COLOR_OF_BOX = GREEN
                elif text_startAgain_rect.collidepoint(event.pos):
                    print("Start Again triggered")
                    resetGame()


            if event.type == pygame.MOUSEBUTTONUP:
                mouseClicked = True

        if game_lost:
            #gameLostScreen()
            elapsed_time = pygame.time.get_ticks() - start_timer
            if elapsed_time > 5000:  # 5 seconds have passed
                resetGame()  # reset the game
                game_lost = False
            else:
                # print(f"Game restarting in {5 - elapsed_time // 1000} seconds")
                countdown_time = 5 - elapsed_time // 1000
                screen.blit(countdown_text_bg, (520, 270))
                test_font = pygame.font.Font('font/DancingScript.ttf', 50)
                countdown_text = test_font.render(str(countdown_time), True, 'black')
                screen.blit(game_lost_text, game_lost_text_rect)
                screen.blit(restarting_in_text, restarting_in_text_rect)
                screen.blit(countdown_text, countdown_text_rect)
                pygame.display.update()
            continue

        player_lost = False
        computer_lost = False
        game_lost = False
        if mouseClicked:
            boxx, boxy = getBoxAtPixel(mousex, mousey)
            if boxx is not None and boxy is not None:
                if grid_colors[boxx][boxy] == PEACH: # can't change the color again if it's already been changed to red, green, pink, or orange
                    grid_colors[boxx][boxy] = COLOR_OF_BOX
                    player_turn = False
                    player_lost = checkIfFailed(boxx, boxy)
                    if not player_lost:
                        computer_lost = computersMove()

                    if player_lost:
                        computer_points += 1
                        print(f"Computer's points: {computer_points}")
                        game_lost = True
                        start_timer = pygame.time.get_ticks()

                    if computer_lost:
                        player_points += 1
                        print(f"Player's points: {player_points}")
                        game_lost = True
                        start_timer = pygame.time.get_ticks()

                    player_turn = True
            mouseClicked = False



        # draw everything
        drawGame()

        pygame.display.update()
        clock.tick(60)

def computersMove():
    randomColor = random.randint(0,3)
    randomColor = colors[randomColor]

    global x, y
    empty_squares = [(x, y) for x in range(NUM_CELLS) for y in range(NUM_CELLS) if grid_colors[x][y] == PEACH]

    if empty_squares:
        x, y = random.choice(empty_squares)
        grid_colors[x][y] = randomColor
        #print(f"Computer painted ({x},{y}) {randomColor}")

    if checkIfFailed(x, y):
            global game_lost, start_timer
            game_lost = True
            start_timer = pygame.time.get_ticks()
            return True
    return False

def drawGame():
    # background
    screen.blit(background_img, (0, 0))

    # text
    screen.blit(text_colors, text_colors_rect)
    screen.blit(text_startAgain, text_startAgain_rect)


    # buckets
    screen.blit(red_bucket, red_bucket_rect)
    screen.blit(orange_bucket, orange_bucket_rect)
    screen.blit(pink_bucket, pink_bucket_rect)
    screen.blit(green_bucket, green_bucket_rect)

    # puzzle square
    drawBoard()
    pygame.draw.rect(screen, 'hotpink', (XMARGIN, YMARGIN, GRID_SIZE, GRID_SIZE), 5)

    # make mouse icon a brush
    mouse_x, mouse_y = pygame.mouse.get_pos()
    screen.blit(CURRENT_BRUSH, (mouse_x - brush_size[0] // 2 + 25, mouse_y - brush_size[1] // 2 + 40))
        #screen.blit(CURRENT_BRUSH, (mouse_x - brush_size[0] // 2, mouse_y - brush_size[1] // 2))


    #scoreboard
    screen.blit(computer_score_text, computer_score_text_rect)
    computer_score_number = test_font.render(str(computer_points), True, RED)
    screen.blit(computer_score_number, computer_score_number_rect)

    screen.blit(player_score_text, player_score_text_rect)
    player_score_number = test_font.render(str(player_points), True, RED)
    screen.blit(player_score_number, player_score_number_rect)



def drawBoard():
    for boxx in range(NUM_CELLS):
        for boxy in range(NUM_CELLS):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            pygame.draw.rect(screen, grid_colors[boxx][boxy], (left, top, BOXSIZE - GAPSIZE, BOXSIZE - GAPSIZE)) # width=1 removed

def getBoxAtPixel(x, y):
    for boxx in range(NUM_CELLS):
        for boxy in range(NUM_CELLS):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return(None, None)

def leftTopCoordsOfBox(boxx, boxy):
    left = XMARGIN + boxx * BOXSIZE
    top = YMARGIN + boxy * BOXSIZE
    return(left, top)

def resetGame():
    global grid_colors, CURRENT_BRUSH, COLOR_OF_BOX
    grid_colors = [[PEACH for _ in range(NUM_CELLS)] for _ in range(NUM_CELLS)]
    CURRENT_BRUSH = red_brush
    COLOR_OF_BOX = RED
    print("Game has been reset!")
    player_turn = True

def checkIfFailed(x, y):
    if x < NUM_CELLS - 1:
        if grid_colors[x][y] == grid_colors[x + 1][y]:
            print("Left neighbor! GAME LOST!")
            return True
    if x > 0:
        if grid_colors[x][y] == grid_colors[x - 1][y]:
            print("Right neighbor! GAME LOST!")
            return True
    if y < NUM_CELLS - 1:
        if grid_colors[x][y] == grid_colors[x][y + 1]:
            print("Top neighbor! GAME LOST!")
            return True
    if y > 0:
        if grid_colors[x][y] == grid_colors[x][y - 1]:
            print("Bottom neighbor! GAME LOST!")
            return True
    return False


if __name__ == "__main__":
    main()