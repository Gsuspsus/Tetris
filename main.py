import pygame
import esper 
import json 
import random

from components import *
from processors import *
from world import world
from constants import FPS

pygame.init()

with open("shapes.json") as f:
    shapes = json.load(f)

world.add_processor(DrawScreenProcessor())
world.add_processor(InputMapperProcessor(), priority=2)
world.add_processor(InputProcessor(), priority=1)
world.add_processor(MovePieceProcessor())

piece_name = random.choice(list(shapes))

shape = world.create_entity(Shape(shapes[piece_name]), GridPosition(4,0), DeltaPosition(0,0), Speed(0.5), Input(
    {
        'escape' : 'QUIT',
        'w' : 'ROTATE',
        "a" : 'MOVE_LEFT',
        'd' : "MOVE_RIGHT"
    }))

while True:
    world.process()
    clock.tick(FPS)