import pygame
import sys
import esper 

from components import *

pygame.init()
screen = pygame.display.set_mode((640,480))



T = Shape([
    [
        [1,1,1],
        [0,1,0],
        [0,1,0]
    ],

    [
        [0,0,1],
        [1,1,1],
        [0,0,1]
    ],

    [
        [0,1,0],
        [0,1,0],
        [1,1,1]
    ],

    [
        [1,0,0],
        [1,1,1],
        [1,0,0]
    ]        

])


SCREEN_WIDTH = 320
SCREEN_HEIGHT = 640

GRID_WIDTH = 10
GRID_HEIGHT = 20

TILE_WIDTH = SCREEN_WIDTH/GRID_WIDTH
TILE_HEIGHT = SCREEN_HEIGHT/GRID_HEIGHT

def draw_block(x,y,height,width):
    pygame.draw.rect(screen, (255,0,0), (x,y,width,height))

def draw_shape(shape):
    for i in range(len(shape)):
        for j in range(len(shape[0])):
            if shape[i][j] == 1:
                draw_block(j*TILE_WIDTH,i*TILE_HEIGHT, TILE_HEIGHT, TILE_WIDTH)


def draw_grid_overlay():
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            pygame.draw.rect(screen, (255,255,255), (j*TILE_WIDTH, i*TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT), 2)

def rotate_right(shape):
    shape.current_rotation += 1
    if shape.current_rotation >= len(shape.rotations):
        shape.current_rotation = 0

def rotate_left(shape):
    shape.current_rotation -= 1
    if shape.current_rotation < 0:
        shape.current_rotation = len(shape.rotations)-1

s = T.rotations[T.current_rotation]

while True:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit() 
            if event.key == pygame.K_w:
                rotate_right(T)

            if event.key == pygame.K_s:
                rotate_left(T)
                
                
    s = T.rotations[T.current_rotation]

    
    draw_shape(s)
    draw_grid_overlay()    


    pygame.display.update()