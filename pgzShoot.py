import pygame
import math
from pygame.locals import *
import pgzrun
from pgzhelper import *
import random

TITLE = "Snoopy"
WIDTH = 973
HEIGHT = 649

snoop = Actor('plane.png')
snoop.scale = 1.1
bird = Actor('bird.png')
pellet = Actor('pellet.png')

snoop.x = 323
snoop.y = 216

bird.x = random.randint(690 , 973)
bird.y = random.randint(0, 649)

velX = .6
velY = .6
bird.velocity = 0

GRAVITY = .2

score = 0

pellets = []

test = False
game_over = False

def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)

def update():
    global score, GRAVITY, test, game_over, velX, velY
    snoop.x = snoop.x + velX
    snoop.y = snoop.y + velY
    snoop.x = clamp(snoop.x, 90, 378)
    snoop.y = clamp(snoop.y, 78, 571)
    if snoop.x == 90 or snoop.x == 378:
        velX = 0
    if snoop.y == 78 or snoop.y == 571:
        velY = 0  
    if keyboard.left:
        velX -= .1
    elif keyboard.right:
        velX += .1
    if keyboard.up:
        velY -= .1
    elif keyboard.down:
        velY += .1
    if keyboard.a:
        velX -= .1
    elif keyboard.d:
        velX += .1
    if keyboard.w:
        velY -= .1
    elif keyboard.s:
        velY += .1
    for pellet in pellets:
        pellet.move_forward(6)
        if pellet.x > 973 or pellet.x < 0:
            pellets.remove(pellet)
        if pellet.y > 649 or pellet.y <0:
            pellets.remove(pellet)
        if bird.collidepoint(pellet.center):
            test = True
            pellets.remove(pellet)
            score += 1
    if test == True:
        bird.velocity += GRAVITY
        bird.y += bird.velocity
        bird.move_forward(2+score/2)
        if bird.y >= 649:
            newBird()
            test = False
            bird.velocity = 0
    bird.move_back(2+score/2)
    if bird.x <= 0:
        score -= 1
        newBird()
    if score < 0:
        game_over = True

def draw():
    screen.clear()
    screen.blit("sky.jpg", (0,0))
    screen.draw.text('score: ' + str(score), color = 'white', topleft=(10,10), fontsize = 30)
    snoop.draw()
    snoop.angle = snoopFace()
    bird.draw()
    for pellet in pellets:
        pellet.draw()
    if game_over:
        screen.fill('black')
        screen.draw.text('GAME OVER', color = 'white', center=(486,325), fontsize = 60)

def on_mouse_down(pos):
    pellet = Actor('pellet.png')
    pellet.angle = snoop.angle
    pellet.pos = snoop.pos
    pellet.move_forward(45)
    pellet.move_right(35)
    pellets.append(pellet)

def snoopFace():
    mouseX, mouseY = pygame.mouse.get_pos()
    snoopAngleRads = math.atan2((mouseY - snoop.y), (mouseX - snoop.x))
    snoopAngleDegs = snoopAngleRads * (180/math.pi)
    return abs(snoopAngleDegs - 360)

def newBird():
    bird.x = random.randint(690 , 973)
    bird.y = random.randint(0, 649)
    
pygame.display.update()
pgzrun.go()
