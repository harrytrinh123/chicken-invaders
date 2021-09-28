import math
import random

import pygame
from pygame import mixer

class Chicken:
    def __init__(self):
        self.imageEnemy = pygame.image.load('./include/chicken.gif').convert_alpha()
        self.x = random.randint(0, 736)
        self.y = random.randint(50, 150)
        self.x_change = 0.1
        self.y_change = 50 
        self.egg = Egg(self.x, self.y)
    def draw(self):
        screen.blit(self.imageEnemy, (self.x, self.y))
    def movement(self):
        self.x += self.x_change
        if self.x <= 0:
            self.x_change = 0.1
            self.y += self.y_change
        elif self.x >= 736:
            self.x_change = -0.1
            self.y += self.y_change
    def isCollisionBullet(self, bulletX, bulletY):
        distance = math.sqrt(math.pow(self.x - bulletX, 2) + (math.pow(self.y - bulletY, 2)))
        if distance < 27:
            return True
        else:
            return False
    
    def throw_egg(self):
        self.egg.x = self.x + 25
        self.egg.y = self.y + 30
class Egg:
    def __init__(self, x, y):
        self.image = pygame.image.load('./include/egg.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (20,20))
        self.x = x
        self.y = y
        self.y_change = 40 
    def drop(self):
        self.y += 0.2
        screen.blit(self.image, (self.x, self.y))
    def isCollistionPlayer(self, playerX, playerY):
        distance = math.sqrt(math.pow(self.x - playerX, 2) + (math.pow(self.y - playerY, 2)))
        if distance < 17:
            return True
        else:
            return False
    

class Player:
    def __init__(self):
        self.imageEnemy = pygame.image.load('./include/ufo.png').convert_alpha()
        self.imageEnemy = pygame.transform.scale(self.imageEnemy, (60, 60))
        self.x = 370
        self.y = 480
        self.x_change = 0
        
    def draw(self):
        screen.blit(self.imageEnemy, (self.x, self.y))
        
    def movement(self):
        self.x += self.x_change
        if self.x <= 0:
            self.x = 0
        elif self.x >= 736:
            self.x = 736

class Bullet:
    def __init__(self) -> None:
        self.bulletImg = pygame.image.load('./include/bullet.png').convert_alpha()
        self.bulletImg = pygame.transform.scale(self.bulletImg, (20,20))
        self.x = 0
        self.y = 480
        self.y_change = 1
        self.state = "ready"
    def set_distance(self, x):
        self.x = x
    def fire_bullet(self):
        if self.state is "fire":
            self.y -= self.y_change
            screen.blit(self.bulletImg, (self.x + 16, self.y))
        if self.y <= 0:
            self.y = 480
            self.state = "ready"
# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('./include/background.png').convert_alpha()
background = pygame.transform.scale(background, (1024,768))

# initialization character
chicken = Chicken()
player = Player()
bullet = Bullet()

num_of_chicken = 10
chickens = []
for i in range(num_of_chicken):
    chicken = Chicken()
    chickens.append(chicken)

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
over_font = pygame.font.Font('freesansbold.ttf', 64)
def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 155))
    screen.blit(score, (x, y))
# game over
def game_over_text():
    over = over_font.render("GAME OVER", True, (255, 255, 155))
    screen.blit(over, (200, 250))

# egg timer
throw_egg_timer = pygame.USEREVENT
pygame.time.set_timer(throw_egg_timer, 3500)
# status game
status_game = "play"
# backdround sound
# Sound
# mixer.music.load("background.wav")
# mixer.music.play(-1)
is_sound = True
# Game Loop
running = True
while running:
    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    
    # Background Image
    screen.blit(background, (0, 0))
    # event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.x_change -= 0.3
            if event.key == pygame.K_RIGHT:
                player.x_change += 0.3
            if event.key == pygame.K_SPACE:
                if bullet.state == 'ready':
                    bulletSound = mixer.Sound("./include/laser.wav")
                    bulletSound.play()
                    bullet.set_distance(player.x + 6)
                    bullet.state = 'fire'
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.x_change = 0
            if event.key == pygame.K_SPACE and status_game is "over":
                score_value = 0
                for i in range(num_of_chicken):
                    chickens[i].y = random.randint(0, 50)
                status_game = "play"
                is_sound = True
        
        if event.type == throw_egg_timer:
            for i in range(num_of_chicken - 2):
                chickens[i].throw_egg()

    player.draw()
    player.movement()
    bullet.fire_bullet()
    for i in range(num_of_chicken):
        chickens[i].draw()
        chickens[i].movement()

    # Collision
    for i in range(num_of_chicken):
        collision_bullet = chickens[i].isCollisionBullet(bullet.x, bullet.y)
        if collision_bullet:
            bullet.y = 480
            bullet.state = "ready"
            chickens[i].x = random.randint(0, 736)
            chickens[i].y = random.randint(50, 150)
            score_value += 1
            explosionSound = mixer.Sound("./include/quad.mp3")
            explosionSound.play()

        collistion_egg = chickens[i].egg.isCollistionPlayer(player.x, player.y)
        if chickens[i].y > 440 or collistion_egg:
            status_game = "over"
            for i in range(num_of_chicken):
                chickens[i].y = 2000
            game_over_text()
        
        chickens[i].egg.drop()
    
    if status_game is "over" and is_sound:
        overSound = mixer.Sound("./include/game-over.wav")
        overSound.play()
        is_sound = False
    show_score(10, 10)
    pygame.display.update()