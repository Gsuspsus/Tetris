import pygame 
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