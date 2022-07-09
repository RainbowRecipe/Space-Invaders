import pygame
import random
import math
from pygame import mixer

# Initialize
pygame.init()

# Game screen and resolution
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('Icon.png')
pygame.display.set_icon(icon)

# Background Image (Static 😢)
background = pygame.image.load('Background02.png')

# Background music
mixer.music.load("backgroundMusic.wav")
mixer.music.play(-1)
mixer.music.set_volume(0.1)

# Sound Effects
explosion_sound = mixer.Sound('ExplosionSoundEffect.wav')
explosion_sound.set_volume(0.3)

bullet_sound = mixer.Sound('LaserSound.wav')

# Player
playerImg = pygame.image.load('Player.png')
playerX = 368
playerY = 480
playerX_speed = 0

# Enemies
enemyImg01 = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg01.append(pygame.image.load('Enemy01.png'))
    # enemyImg02.append(pygame.image.load('Enemy02.png'))

    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('Laserbeam01.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 20
bullet_state = 'ready'

# Player Score
score_value = 0
font = pygame.font.Font('ARCADECLASSIC.TTF', 32)
textX = 10
textY = 10

# Game Over Text
game_over = pygame.font.Font('ARCADECLASSIC.TTF', 64)


# Functions
def show_score(x, y):
    score = font.render("Score " + str(score_value), True, (139, 113, 54))
    screen.blit(score, (x, y))


def game_over_text(x, y):
    game_text = game_over.render("GAME OVER", True, (139, 113, 54))
    final_score = font.render("Score  "  + str(score_value), True, (139, 113, 54))
    screen.blit(game_text, (250, 250))
    screen.blit(final_score, (350, 320))


def player(x, y):
    screen.blit(playerImg, (x, y))


# def playerDeath(enemyX, enemyY, playerX, playerY, i):
#    playertoEnemyDistance = math.sqrt(math.pow(int(enemyX[i]) - playerX, 2) + (math.pow(int(enemyY[i]) - playerY, 2)))
#    if playertoEnemyDistance <= 40:
#        print("Game Over")


def enemy(x, y, i):
    screen.blit(enemyImg01[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 3, y + 10))
    screen.blit(bulletImg, (x + 57, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance <= 50:
        explosion_sound.play()
        return True


# Game Loop
running = True
while running:

    # Screen Color
    # screen.fill((0, 0, 0))

    # Backdrop
    screen.blit(background, (0, 0))

    # Exiting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # checking for keystroke
        if event.type == pygame.KEYDOWN:

            # Horizontal movement
            if event.key == pygame.K_LEFT:
                playerX_speed = -5

            if event.key == pygame.K_RIGHT:
                playerX_speed = 5

            # Vertical movement
            # Deleted

            # Firing the bullet
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        # checking key stroke end
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_speed = 0

    playerX += playerX_speed

    # Player Boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text(200, 250)
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # Collision check
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 100
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        # Spawner
        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

        # Resetting the bullet position
        if bulletY <= -40:
            bulletY = 480
            bullet_state = "ready"

    # Calling the functions
    player(playerX, playerY)
    show_score(textX, textY)
    isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
    # playerDeath(enemyX, enemyY, playerX, playerY, i)

    pygame.display.update()
