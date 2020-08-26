import pygame
import sys
import esper 
import json 

from components import *
from processors import *
from world import world


pygame.init()

with open("shapes.json") as f:
    blocks = json.load(f)["O"]
    world.create_entity(Shape(blocks))

world.add_processor(DrawScreenProcessor())

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit() 
                
                
    world.process()
    
    pygame.display.update()