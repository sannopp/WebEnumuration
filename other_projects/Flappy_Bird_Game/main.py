import random
import sys
import pygame
from pygame.locals import *


FPS = 32
SCREENWIDTH = 800
SCREENHEIGHT = 600
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

GROUND_Y = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = "D:\\GitHub\\Python_Projects\\Flappy_Bird_Game\\source\\Img\\bird.png"
BACKGROUND = "D:\\GitHub\\Python_Projects\\Flappy_Bird_Game\\source\\Img\\backgraund.png"
PIPE = "D:\\GitHub\\Python_Projects\\Flappy_Bird_Game\\source\\Img\\Pipe-Transparent-Images.png"


def welcome_screen():
    """ welcome screen"""
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2
    messagex = int(SCREENWIDTH - GAME_SPRITES['message'].get_width())/2
    messagey = int(SCREENHEIGHT * 0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            # user input...
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            # user input space or up ero key
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUND_Y))
                pygame.display.update()
                FPSCLOCK.tick(FPS)
    pass


def main_game():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENHEIGHT/2)
    basex = 0

    new_pipe1 = get_random_pipe()
    new_pipe2 = get_random_pipe()

    # upper pipes
    upper_pipes = [
        {'x': SCREENWIDTH + 100, 'y': new_pipe1[0]['y']},
        {'x': SCREENWIDTH + 100 + (SCREENWIDTH/2), 'y': new_pipe2[0]['y']}
    ]
    lower_pipes = [
        {'x': SCREENWIDTH + 100, 'y': new_pipe1[1]['y']},
        {'x': SCREENWIDTH + 100 + (SCREENWIDTH / 2), 'y': new_pipe2[1]['y']}
    ]

    pipe_vel_x = -4
    player_vel_y = -9
    player_max_vel_y = 10
    # player_min_vel_y = -8
    player_acc_y = 1

    player_flap_accv = -8
    player_flapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    player_vel_y = player_flap_accv
                    player_flapped = True
                    GAME_SOUNDS['wing'].play()
        crash_test = is_collied(playerx, playery, upper_pipes, lower_pipes)
        if crash_test:
            return

        # score
        player_mid_pos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upper_pipes:
            pipe_mid_pos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipe_mid_pos <= player_mid_pos < pipe_mid_pos + 4:
                score += 1
                print(f'Score:{score}')
                GAME_SOUNDS['point'].play()

        if player_vel_y < player_max_vel_y and not player_flapped:
            player_vel_y += player_acc_y

        if player_flapped:
            player_flapped = False
        player_height = GAME_SPRITES['player'].get_height()
        playery = playery + min(player_vel_y, GROUND_Y - playery - player_height)

        # move pipe to left
        for upperpipe, lowerpipe in zip(upper_pipes, lower_pipes):
            upperpipe['x'] += pipe_vel_x
            lowerpipe['x'] += pipe_vel_x

        # add new pipe
        if 0 < upper_pipes[0]['x'] < 5:
            new_pipe = get_random_pipe()
            upper_pipes.append(new_pipe[0])
            lower_pipes.append(new_pipe[1])
        # remove pipe if it's out of screen
        if upper_pipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upper_pipes.pop(0)
            lower_pipes.pop(0)

        # blit new spriets
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperpipe, lowerpipe in zip(upper_pipes, lower_pipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperpipe['x'], upperpipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerpipe['x'], lowerpipe['y']))
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUND_Y))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        my_digits = [int(x) for x in list(str(score))]
        # my_digits = list(str(score))
        width = 0
        for digit in my_digits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        xoffset = (SCREENWIDTH - width)/2

        for digit in my_digits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (xoffset, SCREENHEIGHT*0.12))
            xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def get_random_pipe():
    """
    generate x,y for two pipes
    :return:
    """
    pipe_height = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3.5
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2*offset))
    pipex = SCREENWIDTH + 10
    y1 = pipe_height - y2 + offset
    pipe = [
        {'x': pipex, 'y': -y1},   # upper pipe
        {'x': pipex, 'y': y2}    # lower pipe
    ]
    return pipe


def is_collied(playerx, playery, upper_pipes, lower_pipes):
    if playery > GROUND_Y - 30 or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upper_pipes:
        pipe_height = GAME_SPRITES['pipe'][0].get_height()
        if playery < pipe_height + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lower_pipes:
        if playery + GAME_SPRITES['player'].get_height() > pipe['y'] and\
                abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False


if __name__ == '__main__':
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy bird game- Aftab Sama')
    GAME_SPRITES['numbers'] = (
        pygame.image.load("D:\\GitHub\\Python_Projects\\Flappy_Bird_Game\\source\\Img\\"
                          "number-0.svg.png").convert_alpha(),
        pygame.image.load("D:\\GitHub\\Python_Projects\\Flappy_Bird_Game\\source\\Img\\"
                          "number-1.svg.png").convert_alpha(),
        pygame.image.load("D:\\GitHub\\Python_Projects\\Flappy_Bird_Game\\source\\Img\\"
                          "number-2.svg.png").convert_alpha(),
        pygame.image.load("D:\\GitHub\\Python_Projects\\Flappy_Bird_Game\\source\\Img\\"
                          "number-3.svg.png").convert_alpha(),
        pygame.image.load("D:\\GitHub\\Python_Projects\\Flappy_Bird_Game\\source\\Img\\"
                          "number-4.svg.png").convert_alpha(),
        pygame.image.load("D:\\GitHub\\Python_Projects\\Flappy_Bird_Game\\source\\Img\\"
                          "number-5.svg.png").convert_alpha(),
        pygame.image.load("D:\\GitHub\\Python_Projects\\Flappy_Bird_Game\\source\\Img\\"
                          "number-6.svg.png").convert_alpha(),
        pygame.image.load("D:\\GitHub\\Python_Projects\\Flappy_Bird_Game\\source\\Img\\"
                          "number-7.svg.png").convert_alpha(),
        pygame.image.load("D:\\GitHub\\Python_Projects\\Flappy_Bird_Game\\source\\Img\\"
                          "number-8.svg.png").convert_alpha(),
        pygame.image.load("D:\\GitHub\\Python_Projects\\Flappy_Bird_Game\\source\\Img\\"
                          "number-9.svg.png").convert_alpha(),
    )
    GAME_SPRITES['message'] = pygame.image.load("D:\\GitHub\\Python_Projects\\Flappy_Bird_Game\\source\\Img\\"
                                                "msg.jpg").convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load("D:\\GitHub\\Python_Projects\\Flappy_Bird_Game\\source\\Img\\"
                                             "base-download.png").convert_alpha()
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
                            pygame.image.load(PIPE).convert_alpha()
                            )
    GAME_SOUNDS['die'] = pygame.mixer.Sound("D:\\GitHub\\Python_Projects\\Flappy_Bird_Game\\source\\Audio\\sfx_die.wav")
    GAME_SOUNDS['hit'] = pygame.mixer.Sound("D:\\GitHub\\Python_Projects\\Flappy_Bird_Game\\source\\Audio\\sfx_hit.wav")
    GAME_SOUNDS['point'] = pygame.mixer.Sound("D:\\GitHub\\Python_Projects\\Flappy_Bird_Game\\source\\Audio\\"
                                              "sfx_point.wav")
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound("D:\\GitHub\\Python_Projects\\Flappy_Bird_Game\\source\\Audio\\"
                                               "sfx_swooshing.wav")
    GAME_SOUNDS['wing'] = pygame.mixer.Sound("D:\\GitHub\\Python_Projects\\Flappy_Bird_Game\\source\\Audio\\"
                                             "sfx_wing.wav")
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcome_screen()
        main_game()
        pass
    pass
