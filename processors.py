import esper
import random
import sys
import pygame 

from world import world
from constants import *
from components import *
from event_queue import EventQueue
from events import *

class DrawScreenProcessor(esper.Processor):
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    def process(self):
        self.screen.fill((0,0,0))
        for ent, (shape, grid_pos) in world.get_components(Shape, GridPosition):
            self.draw_shape(shape, grid_pos.x, grid_pos.y)

        self.draw_grid()
        self.draw_grid_overlay()
        pygame.display.update()

    def draw_shape(self,shape, x,y):
        for i in range(shape.get_height()):
            for j in range(shape.get_width()):
                if shape.get_current_rotation()[i][j] == 1:
                    self.draw_block(x*TILE_WIDTH+j*TILE_WIDTH,y*TILE_HEIGHT+i*TILE_HEIGHT, TILE_HEIGHT, TILE_WIDTH)

    def draw_grid(self):
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                if(grid[i][j] != 0):
                    self.draw_block(j*TILE_WIDTH,i*TILE_HEIGHT,TILE_HEIGHT,TILE_WIDTH)

    def draw_block(self,x,y,height,width):
        pygame.draw.rect(self.screen, (255,0,0), (x,y,width,height))

    def draw_grid_overlay(self):
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                pygame.draw.rect(self.screen, (255,255,255), (j*TILE_WIDTH, i*TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT), 2)

class InputMapperProcessor(esper.Processor):
    def process(self):
        for event in pygame.event.get():
            for ent, input in world.get_component(Input):
                if event.type == pygame.KEYDOWN:
                    action = self.lookup_binding(input.bindings, event.key)
                    if action is not None:
                        input.actions.append(action)
                if event.type == pygame.KEYUP:
                    action = self.lookup_binding(input.bindings, event.key)
                    if action is not None and action in input.actions:
                        input.actions.remove(action)

    def lookup_binding(self, bindings, key, default=None):
        return bindings.get(pygame.key.name(key), default)

class InputProcessor(esper.Processor):
    def process(self):
        for ent, (input, shape, grid_pos) in world.get_components(Input,Shape, GridPosition):
            if 'QUIT' in input.actions:
                pygame.quit()
                sys.exit()
            elif 'ROTATE' in input.actions:
                shape.rotate_right()

            elif 'MOVE_LEFT' in input.actions:
                grid_pos.x -= 1
                grid_pos.x = max(grid_pos.x, 0)
                
            elif 'MOVE_RIGHT' in input.actions:
                grid_pos.x += 1
                grid_pos.x = min(grid_pos.x, GRID_WIDTH-shape.get_width())

            elif 'MOVE_DOWN' in input.actions:
                grid_pos.y +=1 

class MovePieceProcessor(esper.Processor):
    def process(self):
        for ent, (grid_pos, delta_pos, speed) in world.get_components(GridPosition, DeltaPosition, Speed):
            delta_pos.y += speed.amount * (clock.get_time() / 1000)
            if delta_pos.y >= 1:
                grid_pos.y += 1 
                delta_pos.y = 0

class CollisionDetectionProcessor(esper.Processor):
    def process(self):
        for ent, (grid_pos,shape) in world.get_components(GridPosition, Shape):
            if grid_pos.x <= 0:
                event_queue.add(BoundaryHitEvent(LEFT_BOUDNARY))
            elif grid_pos.x >= GRID_WIDTH:
                event_queue.add(BoundaryHitEvent(RIGHT_BOUNDARY))

class LandPieceProcessor(esper.Processor):
    def process(self):
        for ent, (grid_pos, shape) in world.get_components(GridPosition, Shape):
            if grid_pos.y + shape.get_height() == GRID_HEIGHT:
                for i in range(grid_pos.y, grid_pos.y + shape.get_height()):
                    for j in range(grid_pos.x, grid_pos.x + shape.get_width()):
                        if shape.get_current_rotation()[i-grid_pos.y][j-grid_pos.x] != 0:
                            grid[i][j] = 1
                            event_queue.add(SpawnNewPieceEvent())
                        
                world.delete_entity(ent)

class SpawnPieceProcessor(esper.Processor):
    def process(self):
        if event_queue.has_event(SpawnNewPieceEvent):
            piece_name = random.choice(list(shapes))
            shape = world.create_entity(Shape(shapes[piece_name]), GridPosition(4,0), DeltaPosition(0,0), Speed(0.5), Input(bindings))