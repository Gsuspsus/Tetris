import pygame 
import json 
from event_queue import EventQueue

FPS = 60 

GRID_WIDTH = 10
GRID_HEIGHT = 20

SCREEN_WIDTH = 320
SCREEN_HEIGHT = 640

TILE_WIDTH = SCREEN_WIDTH/GRID_WIDTH
TILE_HEIGHT = SCREEN_HEIGHT/GRID_HEIGHT

event_queue = EventQueue()
clock = pygame.time.Clock()
grid = [[0] * GRID_WIDTH for n in range(GRID_HEIGHT)]

with open("shapes.json") as f:
    shapes = json.load(f)