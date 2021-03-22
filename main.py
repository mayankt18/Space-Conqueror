import pygame
import random
import math
from pygame import mixer

# for initialising pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))

# Title and icon
pygame.display.set_caption("Spaceship Game")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)
running = True  # this is to keep the game loop running

# adding sound to the game
mixer.music.load('background.wav')
mixer.music.play(-1)

# adding player 

playerimg = pygame.image.load("player.png")
playerx = 368
playery = 480
playerx_change = 0


def player(x, y):
    screen.blit(playerimg, (x, y))


# score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textx = 10
texty = 10


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# game over

game_over = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    over = game_over.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over, (200, 250))


# adding enemy to the screen

enemyimg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []

num_of_enemies = 6

for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load("enemy.png"))
    enemyx.append(random.randint(0, 736))
    enemyy.append(random.randint(50, 150))
    enemyx_change.append(2)
    enemyy_change.append(30)


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


# bullet

# ready - you can't see the bullet on the screen 
# moving - The bullet is currently moving

bulletimg = pygame.image.load("bullet.png")
bulletx = 0
bullety = 480
bulletx_change = 0
bullety_change = 5
bullet_state = "ready"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "moving"
    screen.blit(bulletimg, (x + 16, y + 10))


# background

background = pygame.image.load("background.png")


# collision

def iscollision(playerx, playery, bulletx, bullety):
    distance = math.sqrt((math.pow(playerx - bulletx, 2)) + (math.pow(playery - bullety, 2)))
    if distance < 27:
        return True
    else:
        return False


# game loop
while running:

    # (R,G,B) = (red, green, blue) color combination
    screen.fill((0, 0, 0))

    # adding background

    screen.blit(background, (0, 0))

    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            running = False

        if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_LEFT:
                playerx_change = -3
            if events.key == pygame.K_RIGHT:
                playerx_change = 3
            if events.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletx = playerx
                    fire_bullet(bulletx, bullety)

        if events.type == pygame.KEYUP:
            if events.key == pygame.K_RIGHT or events.key == pygame.K_LEFT:
                playerx_change = 0

    playerx += playerx_change

    # adding boundaries

    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736

    # enemy movement

    for i in range(num_of_enemies):
        if enemyy[i] > 440:
            for j in range(num_of_enemies):
                enemyy[j] = 2000
            game_over_text()
            break

        if enemyx[i] <= 0:
            enemyx_change[i] = 2
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >= 735:
            enemyx_change[i] = -2
            enemyy[i] += enemyy_change[i]

        collided = iscollision(enemyx[i], enemyy[i], bulletx, bullety)
        if collided:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bullety = 480
            bullet_state = "ready"
            score_value += 1
            enemyx[i] = random.randint(0, 736)
            enemyy[i] = random.randint(50, 150)

        enemyx[i] += enemyx_change[i]

        enemy(enemyx[i], enemyy[i], i)

    # bullet movement

    if bullety == 0:
        bullety = 480
        bullet_state = "ready"

    if bullet_state == "moving":
        fire_bullet(bulletx, bullety)
        bullety -= bullety_change

    # collosion

    player(playerx, playery)
    show_score(textx, texty)

    pygame.display.update()
