import pygame as pg, sys
from settings import *
from overworld import Overworld
from level_test import Level

class Game:
    def __init__(self):
        self.max_level = 0
        self.overworld = Overworld(0, self.max_level , screen, self.create_level)
        self.level = Level(0, screen , self.create_overworld)
        self.status = 'level'

    def create_level(self, curr_level):
        self.level = Level(curr_level, screen, self.create_overworld) 
        self.status = 'level'

    def create_overworld(self, curr_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(curr_level , self.max_level, screen , self.create_level)  
        self.status = 'overworld'

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()       

pg.init()
screen = pg.display.set_mode((WIDTH ,HEIGHT))
clock = pg.time.Clock()
game = Game()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    screen.fill('black')
    game.run()

    pg.display.update()
    clock.tick(60)        
