import pygame
import esper 
import random

from components import *
from processors import *
from world import world
from constants import FPS

pygame.init()

world.add_processor(DrawScreenProcessor(), priority=1)
world.add_processor(InputMapperProcessor(), priority=105)
world.add_processor(InputProcessor(), priority=99)
world.add_processor(MovePieceProcessor(), priority=93)
world.add_processor(LandPieceProcessor(), priority=98)
world.add_processor(SpawnPieceProcessor(), priority=95)
world.add_processor(CollisionDetectionProcessor(), priority=96)
world.add_processor(ClearLineProcessor(), priority=102)
world.add_processor(ScoreProcessor(), priority=90)
world.add_processor(GameOverProcessor(), priority=120)
world.add_processor(SaveScoreProcessor(), priority=8)
world.add_processor(EventMapperProcessor(), priority=103)

player = world.create_entity(Input(bindings))

piece_name = random.choice(list(shapes))
shape = world.create_entity(Shape(shapes[piece_name]), GridPosition(4,0), DeltaPosition(0,0), Speed(0.5))

while True:
    event_queue.clear()
    world.process()
    clock.tick(FPS)