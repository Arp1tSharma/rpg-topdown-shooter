# Computer Graphics Project 
''' 
Arpit Sharma (2K19/CO/079)
Arpan Ekka (2K19/cO/078)
Abhinav Sachdeva (2K19/CO/017)
'''

import pygame as pg
import sys
from os import path

from pygame.constants import HIDDEN
from pygame.draw import rect
from pygame.sprite import Group
from settings import *
from models import *
from tilemap import *
              

class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 1, 2048)
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def draw_rect_alpha(self, surface, color, rect):
        shape_surf = pg.Surface(pg.Rect(rect).size, pg.SRCALPHA)
        pg.draw.rect(shape_surf, color, shape_surf.get_rect())
        surface.blit(shape_surf, rect)    

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
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
        self.screen.blit(text_surface, text_rect)    

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder , 'img')
        self.map_folder = path.join(game_folder , 'maps')
        snd_folder = path.join(game_folder , 'snd')
        music_folder = path.join(game_folder , 'music')

        self.infont = path.join(img_folder, 'STAMPACT.ttf')
        self.ammofont = path.join(img_folder, 'ammo.ttf')
        self.countfont = path.join(img_folder, 'LEVIBRUSH.TTF')
        self.player_face = pg.image.load(path.join(img_folder, FACE_LOGO )).convert_alpha()
        self.title_font = path.join(img_folder, 'ZOMBIE.TTF')
        
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG )).convert_alpha()
        self.bullet_images = {}
        self.gun_images = {}
        self.gun_images['pistol'] = pg.image.load(path.join(img_folder, 'pistol_show.png' )).convert_alpha()
        self.gun_images['shotgun'] = pg.image.load(path.join(img_folder, 'shotgun_show.png' )).convert_alpha()
        self.gun_images['rifle'] = pg.image.load(path.join(img_folder, 'ar_show.png' )).convert_alpha()
        self.ammo_img = pg.image.load(path.join(img_folder, AMMO_IMG )).convert_alpha()
        self.hazard_img = pg.image.load(path.join(img_folder, HAZARD_IMG )).convert_alpha()
        self.bullet_images['lg'] = pg.image.load(path.join(img_folder, BULLET_IMG )).convert_alpha()
        self.bullet_images['sm'] = pg.transform.scale(self.bullet_images['lg'], (10,10))
        self.bullet_images['md'] = pg.transform.scale(self.bullet_images['lg'], (15,15))
        self.mob_img = pg.image.load(path.join(img_folder, ZOMBIE_IMG )).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG )).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE , TILESIZE))
        self.splat = pg.image.load(path.join(img_folder, 'splat green.png')).convert_alpha()
        self.splat = pg.transform.scale(self.splat, (64,64))
        self.go_img = pg.image.load(path.join(img_folder, GAME_OVER )).convert_alpha()
        self.won_img = pg.image.load(path.join(img_folder, SURVIVED_IMAGE)).convert_alpha()
        self.won_img = pg.transform.scale(self.won_img, (WIDTH,HEIGHT))
        self.gun_flashes = []
        for img in MUZZLE_FLASH:
            self.gun_flashes.append(pg.image.load(path.join(img_folder , img)).convert_alpha())
        self.item_images = {}
        for item in ITEM_IMAGES: 
            self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha() 
        # lighting effect
        self.fog = pg.Surface((WIDTH, HEIGHT))
        self.fog.fill(LIGHTGREY)
        self.light_mask = pg.image.load(path.join(img_folder , LIGHT_MASK)).convert_alpha()
        self.light_mask = pg.transform.scale(self.light_mask , LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()
        # sound loading
        pg.mixer.music.load(path.join(music_folder, BG_MUSIC))
        self.effects_sound = {}
        for type in EFFECTS_SOUND:
            self.effects_sound[type] = pg.mixer.Sound(path.join(snd_folder, EFFECTS_SOUND[type]))   
        self.weapon_sounds = {}
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for snd in WEAPON_SOUNDS[weapon]:
                s = pg.mixer.Sound(path.join(snd_folder, snd))
                s.set_volume(0.2)
                self.weapon_sounds[weapon].append(s)
        self.zombie_moan_sounds = []
        for sd in ZOMBIE_MOAN_SOUND:
            s = pg.mixer.Sound(path.join(snd_folder, sd))
            s.set_volume(0.3)
            self.zombie_moan_sounds.append(s)
        self.zombie_hit_sounds =[]
        for snd in ZOMBIE_HIT_SOUND:  
            self.zombie_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))  
        self.player_hit_sounds =[]
        for snd in PLAYER_HIT_SOUND:  
            self.player_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))  
        

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.items = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.effects_sound['level_start'].play()
        self.map = TiledMap(path.join(self.map_folder, 'citymap.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        GUN['pistol']['ammo'] = WEAPONS['pistol']['clip']   
        self.total_zombies = 0
        self.killed = 0
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2 , tile_object.y + tile_object.height / 2)
            if tile_object.name == 'obstacle':
                Obstacle(self , tile_object.x, tile_object.y, tile_object.width , tile_object.height )
            if tile_object.name == 'player':
                self.player = Player(self , obj_center.x , obj_center.y)
            if tile_object.name == 'zombie':
                self.total_zombies += 1
                Zombie( self , obj_center.x , obj_center.y )
            if tile_object.name in ['health','shotgun','rifle']:
                Item(self, obj_center , tile_object.name) 

        self.camera = Camera(self.map.width , self.map.height)
        self.paused = False
        self.night = False

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        self.ne
        pg.mixer.music.play(loops = -1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        #game over
        if len(self.mobs) == 0:
            self.playing = False
        #player collects items
        hits = pg.sprite.spritecollide(self.player , self.items , False)
        for hit in hits:
            if hit.type == "health" and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.effects_sound['health_up'].play()
                self.player.add_health(HEAL_AMOUNT)
            elif hit.type == 'shotgun':
                GUN[hit.type]['equipped'] = True
                GUN[hit.type]['ammo'] += WEAPONS[hit.type]['clip']
                hit.kill()
                self.effects_sound['gun_pickup'].play()
            elif hit.type == 'rifle':    
                GUN[hit.type]['equipped'] = True
                GUN[hit.type]['ammo'] += WEAPONS[hit.type]['clip']
                hit.kill()
                self.effects_sound['gun_pickup'].play()
        # bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs , self.bullets , False , True)
        for mob in hits:
            # hit.health -= WEAPONS[self.player.weapon]['bullet_damage']*len(hits[hit])
            for bullet in hits[mob]:
                mob.health -= bullet.damage
            mob.vel = vec(0,0)
        # zombie hits player
        hits = pg.sprite.spritecollide(self.player, self.mobs , False , collide_hit_rect)
        for hit in hits:
            if random() < 0.7:
                choice(self.player_hit_sounds).play()
            self.player.red_health(MOB_DAMAGE)
            hit.vel = vec(0,0)
            if self.player.target_health <= 0:
                self.playing = False 
        if hits:
            self.player.hit()
            self.player.pos += vec(MOB_KNOCKBACK , 0).rotate(-hits[0].rot)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def display_tiles(self):
        rect_tiles = {}
        i= 0
        for weapon in WEAPONS:
            rect_tiles[weapon] = pg.Rect(110*i + 150, 8 , 95 , 54)
            if GUN[weapon]['ammo'] > 0:
                if weapon == self.player.weapon:
                    pg.draw.rect(self.screen , (0,180,250), rect_tiles[weapon])
                    self.screen.blit(self.gun_images[weapon] , (110*i +150 , 10) )
                else:
                    pg.draw.rect(self.screen , (80,80,80), rect_tiles[weapon])
                    self.screen.blit(self.gun_images[weapon] , (110*i +150 , 10) )
            else:        
                if weapon == self.player.weapon:
                    pg.draw.rect(self.screen , (200,20,20), rect_tiles[weapon])
                    self.screen.blit(self.gun_images[weapon] , (110*i +150 , 10) )
                else:
                    pg.draw.rect(self.screen , (80,0,0), rect_tiles[weapon])
                    self.screen.blit(self.gun_images[weapon] , (110*i +150 , 10) )
            pg.draw.rect(self.screen, (220,220,0) , (rect_tiles[weapon].left - 5, 5 , 105 , 60), 5,2)
            i +=1
            if not GUN[weapon]['equipped']:
                self.draw_rect_alpha(self.screen, (0,0,0,180),rect_tiles[weapon])
                self.draw_text("Locked",self.infont, 10 , (250,250,250) , rect_tiles[weapon].centerx , rect_tiles[weapon].centery , align = "center" )

    def render_fog(self):
        # draw light mask (gradient) onto fog image
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center = self.camera.apply(self.player).center
        self.fog.blit(self.light_mask, self.light_rect)
        self.screen.blit(self.fog, (0,0), special_flags = pg.BLEND_MULT)           

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img , self.camera.apply_rect(self.map_rect))
        # self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite , Zombie):
                sprite.healthBar()
            self.screen.blit(sprite.image , self.camera.apply(sprite))
        # pg.draw.rect(self.screen , WHITE , self.camera.apply(self.player), 2)
        # Fog
        if self.night:
            self.render_fog()
        #HUD func 
        self.display_tiles()
        self.screen.blit(self.player_face , (10 ,0))
        self.player.advanced_health(self.screen , 90, 70)
        if self.paused:
            self.draw_rect_alpha(self.screen, (0,0,0,180) , (60, HEIGHT/8 , 900, 600))
            self.draw_text("PauseD", self.title_font, 105, RED, WIDTH/2, HEIGHT/2, align="center")
            self.draw_text("Press P to Play!", self.infont, 25, WHITE, WIDTH /2, HEIGHT/2 + 100, align="center")
        else:
            self.screen.blit(self.hazard_img, (5 ,HEIGHT - 90))
            self.draw_text(str(self.total_zombies), self.countfont, 25, RED, 15, HEIGHT - 5, align="sw")
            if GUN[self.player.weapon]['ammo'] > 0:
                self.screen.blit(self.ammo_img, (WIDTH - 115 , 5))
                self.draw_text(str(GUN[self.player.weapon]['ammo']), self.ammofont, 30, YELLOW, WIDTH -10, 5, align="ne")
            else:    
                self.screen.blit(self.ammo_img, (WIDTH - 122 , 5))
                self.draw_text("EMPTY", self.ammofont, 25, RED, WIDTH -10, 6, align="ne")
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_p:
                    self.paused = not self.paused
                if event.key == pg.K_1 and self.player.weapon != 'pistol' and GUN['pistol']['equipped']:
                    self.effects_sound['gun_switch'].play()      
                    self.player.weapon = 'pistol'  
                if event.key == pg.K_2 and self.player.weapon != 'shotgun' and GUN['shotgun']['equipped']:
                    self.effects_sound['gun_switch'].play()      
                    self.player.weapon = 'shotgun'        
                if event.key == pg.K_3 and self.player.weapon != 'rifle' and GUN['rifle']['equipped']:
                    self.effects_sound['gun_switch'].play()      
                    self.player.weapon = 'rifle'
                if event.key == pg.K_n:
                    self.night = True            
                

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        self.screen.fill("BLACK")
        
        if self.total_zombies > 0:
            self.survived = False
            self.screen.blit(self.go_img , (-40, 100))
            self.draw_text("Zombies ate your BRAIN!" , self.countfont , 85 , RED ,
                            WIDTH/2, 5 , align = 'n') 
            self.draw_text("Press 'R' to Try Again!" , self.infont , 20 , WHITE ,
                            WIDTH/2, HEIGHT - 50 , align = 's')                
        else:
            self.survived = True
            self.screen.blit(self.won_img, (0,0))
            self.draw_rect_alpha(self.screen , (0, 0 ,0 ,50) , (WIDTH/2 - 20 , 140 , WIDTH/2  , 500))
            self.draw_text("You Survived the Apocalypse!" , self.countfont , 80 , GREEN ,
                            WIDTH/2, 5 , align = 'n') 
            self.draw_text("Press 'C' to Continue!" , self.infont , 15 , WHITE ,
                        WIDTH*3/4 , HEIGHT - 150 , align = 's')                

         
        self.draw_text("Zombies Killed " , self.ammofont , 25 , GREEN ,
                        WIDTH/2, 150 , align = 'nw') 
        self.draw_text("Ammo Used:" , self.ammofont , 25 , WHITE ,
                        WIDTH/2, 200 , align = 'nw') 
        i = 1                
        for wpn in WEAPONS:
            self.draw_text(str(wpn) , self.ammofont , 20 , (250,250,150) ,
                            WIDTH/2 + 50, 200 + i*30 , align = 'nw') 
            self.draw_text(str(WEAPONS[wpn]['clip'] - GUN[wpn]['ammo']) , self.ammofont , 20 , YELLOW ,
                            WIDTH - 50, 200 + i*30 , align = 'ne') 
            GUN[wpn]['ammo'] = WEAPONS[wpn]['clip']                
            i+=1                

        self.draw_text("Percentage Complete" , self.ammofont , 25 , WHITE ,
                        WIDTH/2, 350 , align = 'nw') 
        self.draw_text(str(self.killed) , self.ammofont , 25 , GREEN ,
                        WIDTH - 50, 150 , align = 'ne') 
        
        percnt = (self.killed / (self.killed + self.total_zombies)*100)                
        self.draw_text(f"{percnt:.2f}" + "%" , self.countfont , 25 , GREEN ,
                        WIDTH -50, 350 , align = 'ne') 
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    if event.key == pg.K_r and not self.survived:
                        waiting = False
                    if event.key == pg.K_c and self.survived: 
                        pass


# create the game object
g = Game()
g.show_start_screen()
while True:
    g.run()
    g.show_go_screen()

