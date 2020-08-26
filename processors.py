import esper
import pygame 

from world import world
from constants import *
from components import *
from event_queue import EventQueue

class DrawScreenProcessor(esper.Processor):
    def __init__(self):
        self.screen = pygame.display.set_mode((640,480))
    
    def process(self):
        self.screen.fill((0,0,0))
        for ent, shape in world.get_component(Shape):
            self.draw_shape(shape.rotations[shape.current_rotation])
        self.draw_grid_overlay()

    def draw_shape(self,shape):
        for i in range(len(shape)):
            for j in range(len(shape[0])):
                if shape[i][j] == 1:
                    self.draw_block(j*TILE_WIDTH,i*TILE_HEIGHT, TILE_HEIGHT, TILE_WIDTH)

    def draw_block(self,x,y,height,width):
        pygame.draw.rect(self.screen, (255,0,0), (x,y,width,height))
    
    def draw_grid_overlay(self):
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                pygame.draw.rect(self.screen, (255,255,255), (j*TILE_WIDTH, i*TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT), 2)

    