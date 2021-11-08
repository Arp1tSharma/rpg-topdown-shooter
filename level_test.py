from pygame.constants import K_SPACE
from settings import *
import pygame as pg
from game_data import levels

class Level:
    def __init__(self, curr_level, surface, create_overworld):
        # level setup
        self.display_surface = surface
        self.curr_level = curr_level
        level_data = levels[curr_level]
        level_content = level_data['content']
        self.new_max_level = level_data['unlock']
        self.create_overworld = create_overworld

        # level display
        self.font = pg.font.Font(None,40)
        self.text_surf = self.font.render(level_content, True, 'White')
        self.text_rect = self.text_surf.get_rect(center = (WIDTH/2 , HEIGHT/2))

    def input(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_RETURN]:
            self.create_overworld(self.curr_level, self.new_max_level )
        if keys[pg.K_ESCAPE]:
            self.create_overworld(self.curr_level, 0)   

    def run(self):
        self.input()
        self.display_surface.blit(self.text_surf, self.text_rect)    