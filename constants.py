import pygame 
import json 
from event_queue import EventQueue

FPS = 60 

GRID_WIDTH = 10
GRID_HEIGHT = 20

SCREEN_WIDTH = 440
SCREEN_HEIGHT = 580

INFO_AREA_HEIGHT = 40
INFO_AREA_WIDTH = 200

GAME_WINDOW_WIDTH = SCREEN_WIDTH-INFO_AREA_WIDTH
GAME_WINDOW_HEIGHT = SCREEN_HEIGHT-INFO_AREA_HEIGHT

TILE_WIDTH = int(GAME_WINDOW_WIDTH/GRID_WIDTH)
TILE_HEIGHT = int(GAME_WINDOW_HEIGHT/GRID_HEIGHT)

LEFT_BOUDNARY = 0
RIGHT_BOUNDARY = 1

event_queue = EventQueue()
clock = pygame.time.Clock()
grid = [[0] * GRID_WIDTH for n in range(GRID_HEIGHT)]
score = 0

with open("shapes.json") as f:
    shapes = json.load(f)

bindings = {
        'escape' : 'QUIT',
        'w' : 'ROTATE',
        "a" : 'MOVE_LEFT',
        'd' : "MOVE_RIGHT",
        's' : 'MOVE_DOWN'
    }