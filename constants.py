import pygame 
import json 
from event_queue import EventQueue

FPS = 60 

GRID_WIDTH = 10
GRID_HEIGHT = 20

SCREEN_WIDTH = 240
SCREEN_HEIGHT = 400 

TILE_WIDTH = SCREEN_WIDTH/GRID_WIDTH
TILE_HEIGHT = SCREEN_HEIGHT/GRID_HEIGHT

LEFT_BOUDNARY = 0
RIGHT_BOUNDARY = 1

event_queue = EventQueue()
clock = pygame.time.Clock()
grid = [[0] * GRID_WIDTH for n in range(GRID_HEIGHT)]

with open("shapes.json") as f:
    shapes = json.load(f)

bindings = {
        'escape' : 'QUIT',
        'w' : 'ROTATE',
        "a" : 'MOVE_LEFT',
        'd' : "MOVE_RIGHT",
        's' : 'MOVE_DOWN'
    }