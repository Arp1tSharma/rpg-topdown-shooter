import pygame as pg
from game_data import levels

class Node(pg.sprite.Sprite):
    def __init__(self, pos, unlocked , icon_speed):
        super().__init__()
        
        self.image = pg.Surface((100,80))
        if unlocked:
            self.image.fill('red')
        else:
            self.image.fill('grey')    
        self.rect = self.image.get_rect(center = pos)

        self.detection_zone = pg.Rect(self.rect.centerx-icon_speed/2,self.rect.centery-icon_speed/2,icon_speed,icon_speed)

class Icon(pg.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.pos = pos
        self.image = pg.Surface((30,30))
        self.image.fill('blue')
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
                node_sprite = Node(node_data['node_pos'], True ,self.speed)
            else:
                node_sprite = Node(node_data['node_pos'], False ,self.speed)     
            
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
                self.move_direction = self.get_movement_data(1)
                self.curr_level += 1
                self.moving = True
            elif keys[pg.K_LEFT] and self.curr_level >0:  
                self.move_direction = self.get_movement_data(-1)
                self.curr_level -= 1
                self.moving = True 
            elif keys[pg.K_SPACE] :
                self.create_level(self.curr_level)   
                  

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
        self.draw_paths()
        self.update_icon_pos()
        self.icon.update()
        self.input()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)  