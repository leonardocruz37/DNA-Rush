import pygame
import math
from random import randint

# Initializing
pygame.init()

# Set up the screen
window_icon = pygame.image.load('window_icon.png')
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('DNA Rush')
pygame.display.set_icon(window_icon)

# Score
font = pygame.font.Font('freesansbold.ttf', 24)
score_value = 0
level_value = 0
def show_score(score_value):
    text = font.render('Score: ' + str(score_value) + ', Level: ' + str(level_value), True, (255, 255, 255))
    screen.blit(text, (10, 10))

# Try harder
font = pygame.font.Font('freesansbold.ttf', 24)
def try_harder():
    text = font.render('Try harder :)', True, (255, 255, 255))
    screen.blit(text, (340, 320))

# Game over
font_over = pygame.font.Font('freesansbold.ttf', 64)
def game_over():
    text = font_over.render('GAME OVER', True, (255, 255, 255))
    screen.blit(text, (200, 250))

# Set up the player
player_icon = pygame.image.load('player.png')
player_X = 400
player_Y = 520
player_change_X = 0
player_change_Y = 0

def player(x, y):
    screen.blit(player_icon, (x, y))

# Set up the DNA bases
baseA_icon = pygame.image.load('A.png')
baseC_icon = pygame.image.load('C.png')
baseT_icon = pygame.image.load('T.png')
baseG_icon = pygame.image.load('G.png')
icon_list = [baseA_icon, baseC_icon, baseT_icon, baseG_icon]
name_list = ['A', 'C', 'T', 'G']

base_name = []
base_icon = []
base_X = []
base_Y = []

def base(base, x, y):
    screen.blit(base, (x, y))

# Set up enemy
enemy_icon = pygame.image.load('virus_64.png')
enemy_X = []
enemy_Y = []

def enemy(x, y):
    screen.blit(enemy_icon, (x, y))

# Detect collision
def isCollision(x1, x2, y1, y2, enemy = False):
    if enemy:
        collided = 55
    else:
        collided = 34
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    if distance < collided:
        return True
    else:
        return False

# Configs
base_change = 0.1
enemy_change = 0.05

final_score = []
running = True
over = False
while running:

    # Ajust the speed per number of images on screen to remove lag
    #add_speed = (len(enemy_X) + len(base_X))/150
    add_speed = 0

    # Background
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_change_X = -0.4 + add_speed
            if event.key == pygame.K_RIGHT:
                player_change_X = 0.4 + add_speed
            if event.key == pygame.K_UP:
                player_change_Y = -0.4 + add_speed
            if event.key == pygame.K_DOWN:
                player_change_Y = 0.4 + add_speed
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player_change_X = 0
                player_change_Y = 0


    # Player
    player_X += player_change_X
    player_Y += player_change_Y

    if player_X <= 0:
        player_X = 0
    elif player_X >= 736:
        player_X = 736
    elif player_Y <= 0:
        player_Y = 0
    elif player_Y >= 536:
        player_Y = 536

    player(player_X, player_Y)

    # Bases
    if randint(1,600) == 1:
        r = randint(0,3)
        base_icon.append(icon_list[r])
        base_name.append(name_list[r])
        base_X.append(randint(0, 768))
        base_Y.append(0)

    for i in range(len(base_icon)-1):
        base_Y[i] += base_change + add_speed
        base(base_icon[i], base_X[i], base_Y[i])
        if base_Y[i] >= 600:
            base_icon.pop(i)
            base_name.pop(i)
            base_X.pop(i)
            base_Y.pop(i)
        if isCollision(player_X, base_X[i], player_Y, base_Y[i]):
            if base_name[i] == 'C' or base_name[i] == 'G':
                score_value += 1
            if base_name[i] == 'A':
                score_value += 5
            if base_name[i] == 'T':
                score_value += 10

            base_icon.pop(i)
            base_name.pop(i)
            base_X.pop(i)
            base_Y.pop(i)

    # Score
    show_score(score_value)


    # Enemy
    if randint(1,1300) == 1:
        enemy_X.append(randint(0, 736))
        enemy_Y.append(0)

    for i in range(len(enemy_X)-1):
        enemy_Y[i] += enemy_change + add_speed
        enemy(enemy_X[i], enemy_Y[i])
        if enemy_Y[i] >= 600:
            enemy_X.pop(i)
            enemy_Y.pop(i)
        if isCollision(player_X, enemy_X[i], player_Y, enemy_Y[i], True):
            over = True
            final_score.append(score_value)

    # Dificulty
    if score_value >= 100 and score_value < 200:
        enemy_change = 0.2
        level_value = 1
    elif score_value >= 200 and score_value < 300:
        enemy_change = 0.4
        level_value = 2
    elif score_value >= 300 and score_value < 500:
        enemy_change = 0.6
        level_value = 3
    elif score_value >= 500 and score_value < 1000:
        enemy_change = 0.8
        level_value = 4
    elif score_value >= 1000:
        enemy_change = 1
        level_value = 5

    if over:
        screen.fill((0, 0, 0))
        if len(final_score) > 1:
            final_score.pop(1)
        show_score(final_score[0])
        game_over()
        try_harder()

    pygame.display.update()
