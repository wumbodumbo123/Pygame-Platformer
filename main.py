import pygame
import sys

import sys

import pygame

pygame.init()

width, height = 640, 400
TITLE = "rpg"
clock = pygame.time.Clock()
SCREEN = pygame.display.set_mode((width, height))
pygame.display.set_caption(TITLE)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FloorX = 0
FloorY = 380
FloorSizeX = 640
FloorSizeY = 20
JTime = False
timer_interval = 200  # 0.5 seconds
timer_event = pygame.USEREVENT + 1
BlocksSizeY: list[int] = [0, 0]
BlocksSizeX: list[int] = [0, 0]
BlocksY: list[int] = [0, 0]
BlocksX: list[int] = [0, 0]
PlY = 40
PlX = 40
numBlocks = 2
FloorRect = pygame.Rect(FloorX, FloorY, FloorSizeX, FloorSizeY)
Block = pygame.Rect(500, 240, 140, 40)
RectValues = [FloorRect, Block]
JumpTrue = True
jumping = False
Grav = 1
JumpVel = 1
gravityTrue = None


def jump():
    global jumping
    if jumping:
        player.velY -= player.speed * 0.25
        for num in range(numBlocks):
            if abs(RectValues[num].top - player.rect.bottom) < 10 and player.velY < 0:
                jumping = False


def gravity():
    global gravityTrue
    if gravityTrue:
        player.velY += Grav
    for num in range(numBlocks):
        if abs(RectValues[num].top - player.rect.bottom) < 10 and player.velY < 0:
            gravityTrue = False
            player.y = RectValues[num].y - PlY


# player stuff
class player:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.rect = pygame.Rect(int(self.x), int(self.y), PlX, PlY)
        self.color = (0, 0, 255)
        self.velX = 0
        self.velY = 0
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 4

    def draw(self, s):
        pygame.draw.rect(s, self.color, self.rect)

    def update(self):
        if self.left_pressed and not self.right_pressed:
            self.velX = -self.speed
        if self.right_pressed and not self.left_pressed:
            self.velX = self.speed

        self.x += self.velX
        self.y += self.velY

        self.rect = pygame.Rect(int(self.x), int(self.y), PlX, PlY)


player = player(width / 2, height / 2)
player.y = RectValues[0].y - PlY


def PlCollision():
    global jumping

    # Screen border collision
    if player.rect.right >= width:
        player.x = width - PlX
    if player.rect.left <= 0:
        player.x = 0
    if player.rect.bottom >= height:
        player.y = height - PlY
    if player.rect.top <= 0:
        player.y = 0

    # block collision
    CollisionTolerance = 10
    for num in range(numBlocks):
        if player.rect.colliderect(RectValues[num]):
            print("collide")
            print(player.velY)
            if abs(RectValues[num].top - player.rect.bottom) < CollisionTolerance and player.velY < 0:
                player.y = RectValues[num].y - PlY
                jumping = False
                player.velY = JumpVel
            if abs(RectValues[num].bottom - player.rect.top) < CollisionTolerance and player.velY > 0:
                player.velY = 0
            if abs(RectValues[num].left - player.rect.right) < CollisionTolerance and player.velX > 0:
                player.velX = 0
            if abs(RectValues[num].right - player.rect.left) < CollisionTolerance and player.velX < 0:
                player.velX = 0


def movement():
    global jumping
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a:
            if not player.x <= 0:
                player.left_pressed = True
        if event.key == pygame.K_d:
            if not player.x >= width - PlX:
                player.right_pressed = True
        if event.key == pygame.K_w:
            jumping = True

    # Keyup
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_a:
            player.left_pressed = False
            player.velX = 0
        if event.key == pygame.K_d:
            player.right_pressed = False
            player.velX = 0
        if event.key == pygame.K_w:
            player.up_pressed = False


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        movement()

    # any forever loop things

    PlCollision()

    # forever loop functions
    jump()
    gravity()

    # draw anything
    SCREEN.fill((12, 24, 36))
    player.draw(SCREEN)
    pygame.draw.rect(SCREEN, RED, FloorRect)
    BlocksSizeX[0] = FloorSizeX
    BlocksSizeY[0] = FloorSizeY
    BlocksY[0] = FloorY
    BlocksX[0] = FloorX
    pygame.draw.rect(SCREEN, RED, Block)

    # block x and y values
    BlocksSizeX[1] = 140
    BlocksSizeY[1] = 40
    BlocksY[1] = 240
    BlocksX[1] = 500

    # update
    player.update()
    pygame.display.flip()

    clock.tick(60)