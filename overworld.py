import pygame as pg
from game_data import levels
from os import path

from settings import HEIGHT, WIDTH

game_folder = path.dirname(__file__)
snd_folder = path.join(game_folder , 'snd')
img_folder = path.join(game_folder , 'img')

def draw_rect_alpha(surface, color, rect):
        shape_surf = pg.Surface(pg.Rect(rect).size, pg.SRCALPHA)
        pg.draw.rect(shape_surf, color, shape_surf.get_rect())
        surface.blit(shape_surf, rect)    

def draw_text(screen, text, font_name, size, color, x, y, align="nw"):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if align == "nw":
        text_rect.topleft = (x, y)
    if align == "ne":
        text_rect.topright = (x, y)
    if align == "sw":
        text_rect.bottomleft = (x, y)
    if align == "se":
        text_rect.bottomright = (x, y)
    if align == "n":
        text_rect.midtop = (x, y)
    if align == "s":
        text_rect.midbottom = (x, y)
    if align == "e":
        text_rect.midright = (x, y)
    if align == "w":
        text_rect.midleft = (x, y)
    if align == "center":
        text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

class Node(pg.sprite.Sprite):
    def __init__(self, pos, unlocked , icon_speed ,imgpath):
        super().__init__()
        
        if unlocked:
            self.status = 'avaialble'
        else:
            self.status = 'locked'
 
        self.image = pg.image.load(path.join(img_folder, imgpath)).convert_alpha()
        self.rect = self.image.get_rect(center = pos)

        self.detection_zone = pg.Rect(self.rect.centerx-icon_speed/2,self.rect.centery-icon_speed/2,icon_speed,icon_speed)

    def update(self):
        if self.status == 'locked':
            tint_surf = self.image.copy()
            tint_surf.fill('black', None , pg.BLEND_RGBA_MULT )
            self.image.blit(tint_surf, (0,0))    

class Icon(pg.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.pos = pos
        self.image = pg.image.load(path.join(img_folder ,'icon.png')).convert_alpha()

        self.rect = self.image.get_rect(center = pos)

    def update(self):
        self.rect.center = self.pos    

class Overworld:
    def __init__(self, start_level , max_level , surface, create_level):
        
        #set up
        self.display_surface = surface
        self.max_level = max_level
        self.curr_level = start_level
        self.create_level = create_level


        # movement logic
        self.moving = False
        self.move_direction = pg.math.Vector2(0,0) 
        self.speed = 8


        # sprites
        self.setup_nodes()
        self.setup_icon()

    def setup_nodes(self):
        self.nodes = pg.sprite.Group()

        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite = Node(node_data['node_pos'], True ,self.speed , node_data['node_graphics'])
            else:
                node_sprite = Node(node_data['node_pos'], False ,self.speed , node_data['node_graphics'])     
            
            self.nodes.add(node_sprite)

    def draw_paths(self):
        if self.max_level > 0:
            points = [node['node_pos'] for ind , node in enumerate(levels.values()) if ind <= self.max_level]
            # print(points)
            pg.draw.lines(self.display_surface , 'red' ,False,  points, 6 )

    def setup_icon(self):
        self.icon = pg.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.curr_level].rect.center)
        self.icon.add(icon_sprite)

    def input(self):
        keys = pg.key.get_pressed()
        if not self.moving:
            if keys[pg.K_RIGHT] and self.curr_level < self.max_level:
                snd = pg.mixer.Sound(path.join(snd_folder, 'move_icon.wav'))
                snd.play()
                self.move_direction = self.get_movement_data(1)
                self.curr_level += 1
                self.moving = True
            elif keys[pg.K_LEFT] and self.curr_level >0:  
                snd = pg.mixer.Sound(path.join(snd_folder, 'move_icon.wav'))
                snd.play()
                self.move_direction = self.get_movement_data(-1)
                self.curr_level -= 1
                self.moving = True 
            elif keys[pg.K_RETURN]:
                snd = pg.mixer.Sound(path.join(snd_folder, 'start_stage.wav'))
                snd.play()
                self.create_level(self.curr_level)   
                  
    def draw_bg(self):
        self.bg_img = pg.image.load(path.join(img_folder, levels[self.curr_level]['bg_img'])).convert_alpha()
        self.display_surface.blit(self.bg_img , (0,0))
        draw_rect_alpha(self.display_surface , (160,160,160,80) , (20,65, WIDTH -60 , HEIGHT - 120))
        draw_text(self.display_surface, "Press Enter to Begin!", path.join(img_folder, 'LEVIBRUSH.TTF'), 20 ,'White' , WIDTH/2 , HEIGHT - 30 , 's')
        draw_text(self.display_surface, "Choose a Location!", path.join(img_folder, 'ammo.ttf'), 80 ,'Red' , WIDTH/2 , 10 , 'n')


    def get_movement_data(self, dir):
        start = pg.math.Vector2(self.nodes.sprites()[self.curr_level].rect.center)
        if dir == 1:
            end = pg.math.Vector2(self.nodes.sprites()[self.curr_level + 1].rect.center)
        elif dir == -1:
            end = pg.math.Vector2(self.nodes.sprites()[self.curr_level - 1].rect.center)

        return (end - start).normalize()

    def update_icon_pos(self):
        if self.moving and self.move_direction:
            self.icon.sprite.pos += self.move_direction * self.speed
            target_node = self.nodes.sprites()[self.curr_level]
            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.move_direction = pg.math.Vector2(0,0)

    def run(self):
        self.update_icon_pos()
        self.draw_bg()
        self.draw_paths()
        self.nodes.update()
        self.icon.update()
        self.input()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)  