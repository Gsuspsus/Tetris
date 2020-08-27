import pygame
import esper 
import json 
import random

from components import *
from processors import *
from world import world
from constants import FPS

clock = pygame.time.Clock()

pygame.init()

with open("shapes.json") as f:
    shapes = json.load(f)

world.add_processor(DrawScreenProcessor())
world.add_processor(InputMapperProcessor(), priority=2)
world.add_processor(InputProcessor(), priority=1)

piece_name = random.choice(list(shapes))

shape = world.create_entity(Shape(shapes[piece_name]), Input(
    {'escape' : 'QUIT',
    'w' : 'ROTATE',
    }) )

while True:
    world.process()
    clock.tick(FPS)