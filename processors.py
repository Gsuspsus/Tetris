import esper
import pygame
import random
import sys
from datetime import datetime

from world import world
from constants import *
from components import *
from event_queue import EventQueue
from events import *

class DrawScreenProcessor(esper.Processor):
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
    def process(self):
        self.screen.fill((0, 0, 0))
        for ent, (shape, grid_pos) in world.get_components(Shape, GridPosition):
            self.draw_shape(shape, grid_pos.x, grid_pos.y)

        self.draw_grid()
        self.draw_grid_overlay()
        self.draw_score()
        self.draw_next_up()
        pygame.display.update()

    def draw_shape(self, shape, x, y):
        for i in range(shape.get_height()):
            for j in range(shape.get_width()):
                if shape.get_current_rotation()[i][j] == 1:
                    self.draw_block(
                        x*TILE_WIDTH+j*TILE_WIDTH, INFO_AREA_HEIGHT+y*TILE_HEIGHT+i*TILE_HEIGHT, TILE_HEIGHT, TILE_WIDTH, random.choice(list(COLORS.values())))

    def draw_grid(self):
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                if(grid[i][j] != 0):
                    self.draw_block(j*TILE_WIDTH, INFO_AREA_HEIGHT+i*TILE_HEIGHT,
                                    TILE_HEIGHT, TILE_WIDTH, (0,0,255))

    def draw_block(self, x, y, height, width,color=(255,0,0)):
        pygame.draw.rect(self.screen, color, (x, y, width, height))

    def draw_grid_overlay(self):
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                pygame.draw.rect(self.screen, (255, 255, 255),
                                 (j*TILE_WIDTH, INFO_AREA_HEIGHT+i*TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT), 1)

    def draw_score(self):
       textsurface = self.font.render(str(score), False, (0, 255, 0))
       self.screen.blit(textsurface,(GAME_WINDOW_WIDTH//2-textsurface.get_width()//2,0))

    def draw_next_up(self):
        spawner = world.component_for_entity(entities_map['spawner'], PieceContainer)
        shape = Shape(shapes[spawner.next()])
        for i in range(shape.get_height()):
            for j in range(shape.get_width()):
                if shape.get_current_rotation()[i][j] == 1:
                    self.draw_block(
                        j*TILE_WIDTH+GAME_WINDOW_WIDTH+INFO_AREA_WIDTH//2, i*TILE_HEIGHT+SCREEN_HEIGHT//3, TILE_HEIGHT,TILE_HEIGHT)


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

class EventMapperProcessor(esper.Processor):
    def process(self):
        for ent, input in world.get_component(Input):
            for action in input.actions:
                event = events_map.get(action, None)
                if event is not None:
                    event_queue.add(event)


class InputProcessor(esper.Processor):
    def __init__(self):
        self.timeout_period = 125
        self.ticks_since_last = 0

    def process(self):
        if(pygame.time.get_ticks() - self.ticks_since_last) > self.timeout_period:
            if event_queue.has_event(QuitGameEvent):
                pygame.quit()
                sys.exit()
            for ent, (shape, grid_pos) in world.get_components(Shape, GridPosition):
                if event_queue.has_event(RotatePieceEvent):
                    shape.rotate_right()
                    self.ticks_since_last = pygame.time.get_ticks()+50
                elif event_queue.has_event(MovePieceLeftEvent):
                    blocked = False
                    for i in range(shape.get_height()):
                        for j in range(shape.get_width()):
                            if grid[grid_pos.y+i][max(grid_pos.x-1,0)] != 0:
                                blocked = True

                    if not blocked:
                        grid_pos.x -= 1
                        grid_pos.x = max(grid_pos.x, 0)
                        self.ticks_since_last = pygame.time.get_ticks()

                elif event_queue.has_event(MovePieceRightEvent):
                    blocked = False
                    for i in range(shape.get_height()):
                        for j in range(shape.get_width()):
                            if grid[grid_pos.y+i][min(grid_pos.x+shape.get_width(), GRID_WIDTH-1)] != 0:
                                blocked = True

                    if not blocked:
                        grid_pos.x += 1
                        grid_pos.x = min(grid_pos.x, GRID_WIDTH-shape.get_width())
                        self.ticks_since_last = pygame.time.get_ticks()

                elif event_queue.has_event(MovePieceDownEvent):
                    grid_pos.y += 1
                    self.ticks_since_last = pygame.time.get_ticks()


class MovePieceProcessor(esper.Processor):
    def process(self):
        for ent, (grid_pos, delta_pos, speed) in world.get_components(GridPosition, DeltaPosition, Speed):
            delta_pos.y += speed.amount * (clock.get_time() / 1000)
            if delta_pos.y >= 1:
                grid_pos.y += 1
                delta_pos.y = 0


class CollisionDetectionProcessor(esper.Processor):
    def process(self):
        for ent, (grid_pos, shape) in world.get_components(GridPosition, Shape):
            if grid_pos.x <= 0:
                event_queue.add(BoundaryHitEvent(LEFT_BOUDNARY))
            elif grid_pos.x >= GRID_WIDTH:
                event_queue.add(BoundaryHitEvent(RIGHT_BOUNDARY))

class LandPieceProcessor(esper.Processor):
    def process(self):
        hit = False
        for ent, (grid_pos, shape) in world.get_components(GridPosition, Shape):
            if grid_pos.y + shape.get_height() >= GRID_HEIGHT:
                hit = True
            else:
                for i in range(grid_pos.y, grid_pos.y + shape.get_height()):
                    for j in range(grid_pos.x, grid_pos.x + shape.get_width()):
                        if shape.get_current_rotation()[i-grid_pos.y][j-grid_pos.x] != 0:
                            if grid[i+1][j] != 0:
                                hit = True
            if hit:
                for i in range(grid_pos.y, grid_pos.y + shape.get_height()):
                    for j in range(grid_pos.x, grid_pos.x + shape.get_width()):
                        if shape.get_current_rotation()[i-grid_pos.y][j-grid_pos.x] != 0:
                            grid[i][j] = 1
                world.delete_entity(ent)
                spawner = world.component_for_entity(entities_map['spawner'], PieceContainer)
                spawner.current = spawner.pop()

class SpawnPieceProcessor(esper.Processor):
    def process(self):
        for ent, container in world.get_component(PieceContainer):
            if container.current != None:
                if container.remainig_length == 0:
                    container.bag.reset_bag()
                piece_name = container.current
                shape = world.create_entity(Shape(shapes[piece_name]), GridPosition(
                    4, 0), DeltaPosition(0, 0), Speed(0.5), Input(bindings))
                container.current = None

            
class SaveScoreProcessor(esper.Processor):
    def process(self):
        if event_queue.has_event(SaveScoreEvent):
            with open('score.txt', 'a') as f:
                date = datetime.now().strftime("(%d/%m/%Y %H:%M:%S)")
                f.write(date + " : " + str(score) + "\n")
            world.remove_processor(SaveScoreProcessor)
            

class ScoreProcessor(esper.Processor):
    def process(self):
        global score
        if event_queue.has_event(LineCleared):
            score += 1

class ClearLineProcessor(esper.Processor):
    def process(self):
        line = None
        for i in range(GRID_HEIGHT):
            if grid[i][0] == 0:
                continue
            else:
                for j in range(GRID_WIDTH):
                    if grid[i][j] == 0:
                        break
                    elif j == GRID_WIDTH-1:
                        line = i

        if line is not None:
            self.move_lines_down(line)
            event_queue.add(LineCleared())

    def move_lines_down(self, target_line):
        above_rows = [[0] * GRID_WIDTH for n in range(target_line)] 
        for i in range(target_line):
            for j in range(GRID_WIDTH):
                above_rows[i][j] = grid[i][j]
            
        for i in range(len(above_rows)):
            for j in range(len(above_rows[0])):
                grid[i+1][j] = above_rows[i][j]

class GameOverProcessor(esper.Processor):
    def process(self):
        for i in range(GRID_WIDTH):
            if grid[0][i] != 0:
                world.remove_processor(SpawnPieceProcessor)
                event_queue.add(SaveScoreEvent())