import pygame
import sys
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

piece_name = random.choice(list(shapes))

shape = world.create_entity(Shape(shapes[piece_name]), Input({'a' : 'ROTATE_LEFT'}) )

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            else:
                name = pygame.key.name(event.key).upper()
                if name in shapes.keys():
                    world.delete_entity(shape)
                    shape = world.create_entity(Shape(shapes[name]), Input({'a' : 'ROTATE_LEFT'}) )
                
                
    world.process()
    pygame.display.update()
    clock.tick(FPS)