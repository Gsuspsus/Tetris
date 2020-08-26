import pygame
import sys
import esper 
import json 

from components import *
from processors import *
from world import world


pygame.init()

with open("shapes.json") as f:
    blocks = json.load(f)["T"]
    print(blocks)
    world.create_entity(Shape(blocks))


world.add_processor(DrawPieceProcessor())

while True:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit() 
                
                
    world.process()
    
    pygame.display.update()