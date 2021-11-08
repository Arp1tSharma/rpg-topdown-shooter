import pygame as pg
from random import uniform,choice, randint , random
from pygame import sprite
from settings import *
import pytweening as tween
from itertools import chain

# vector initialization
vec = pg.math.Vector2

# for better collisions
def collide_hit_rect(one , two):
    return one.hit_rect.colliderect(two.rect)

def collide_with_walls(sprite , group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, sprite.game.walls, False , collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x    
    if dir == 'y':
        hits = pg.sprite .spritecollide(sprite, sprite.game.walls , False , collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Player(pg.sprite.Sprite):
    def __init__(self , game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        # self.image = pg.Surface((TILESIZE , TILESIZE ))
        self.image = game.player_img
        self.health = PLAYER_HEALTH
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0,0)
        self.pos = vec( x, y)
        self.max_health = PLAYER_HEALTH
        self.rot = 0
        self.last_shot = 0
        self.health_ratio = self.max_health / BAR_LENGTH
        self.target_health = self.max_health
        self.hc_speed = 10
        self.weapon = 'pistol'
        self.damaged = False

    def add_health(self, amount):
        self.target_health += amount
        if self.target_health > self.max_health:
            self.target_health = self.max_health

    def red_health(self,amount):
        self.target_health -= amount
        if self.target_health <= 0:
            self.target_health = 0

    def advanced_health(self , surf, x, y):

        transition_width = 0
        bar_clr = GREEN
        transition_clr = WHITE

        if self.health < self.target_health:
            self.health += self.hc_speed
            transition_width = int((self.target_health - self.health)/self.health_ratio)
            transition_clr = (0, 200, 200)

        if self.health > self.target_health:
            self.health -= self.hc_speed
            transition_width = int((self.target_health - self.health)/self.health_ratio)
            transition_clr = (100, 0 , 0)

        if self.health < self.max_health*0.30:
            bar_clr = RED
        elif self.health < self.max_health*0.70:
            bar_clr = YELLOW
        else:
            bar_clr = GREEN  
              
        health_bar_rect = pg.Rect(x, y, self.health/self.health_ratio, 25)
        transition_bar_rect = pg.Rect(x+int(self.health/self.health_ratio), y, transition_width, 25)
        
        pg.draw.rect(surf , bar_clr , health_bar_rect)
        pg.draw.rect(surf , transition_clr , transition_bar_rect)
        pg.draw.rect(surf , (255,255,255), (x,y , BAR_LENGTH , 25),2)

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0,0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec(PLAYER_SPEED , 0).rotate(-self.rot)  
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-PLAYER_SPEED/2 , 0).rotate(-self.rot)  
        if keys[pg.K_SPACE] or keys[pg.K_KP_0]:
            self.shoot()
            
    def shoot(self):      
        now = pg.time.get_ticks()
        if now - self.last_shot > WEAPONS[self.weapon]['rate']:
            self.last_shot = now
            if GUN[self.weapon]['ammo'] > 0:
                dir = vec(1,0).rotate(-self.rot)
                pos = self.pos + GUN_OFFSET.rotate(-self.rot)
                self.vel = vec(-WEAPONS[self.weapon]['kickback'], 0).rotate(-self.rot)
                for i in range(WEAPONS[self.weapon]['bullet_count']):
                    spread = uniform(-WEAPONS[self.weapon]['spread'], WEAPONS[self.weapon]['spread'])
                    snd = choice(self.game.weapon_sounds[self.weapon])
                    if snd.get_num_channels() > 2:
                        snd.stop()
                    snd.play()    
                    Bullets(self.game , pos , dir.rotate(spread) , WEAPONS[self.weapon]['bullet_damage'] ) 
                MuzzleFlash(self.game , pos) 
                GUN[self.weapon]['ammo'] -= 1
            else:
                snd = self.game.effects_sound['empty']
                if snd.get_num_channels() > 2:
                    snd.stop()
                snd.play()   
            # self.vel.y = PLAYER_SPEED                          

    def hit(self):
        self.damaged = True
        self.damage_alpha = chain(DAMAGE_ALPHA * 3)

    def update(self):
        self.get_keys()
        self.rot = (self.rot + self.game.dt * self.rot_speed) % 360   
        self.image = pg.transform.rotate(self.game.player_img , self.rot)
        if self.damaged:
            # dmg_image = self.image.copy()
            try:
                self.image.fill((255 , 100, 100, next(self.damage_alpha)), special_flags = pg.BLEND_RGBA_MULT)
            except:
                self.damaged = False    


        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel*self.game.dt;
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls , 'y')
        self.rect.center = self.hit_rect.center 
        
class Wall(pg.sprite.Sprite):
    def __init__(self , game , x ,y):
        self._layer = WALL_LAYER
        self.groups = game.all_sprites , game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x*TILESIZE
        self.rect.y = y*TILESIZE

class Obstacle(pg.sprite.Sprite):
    def __init__(self , game , x ,y , w, h):
        self._layer = WALL_LAYER
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x , y , w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Zombie(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self , self.groups)
        self.image = game.mob_img.copy()
        self.game = game
        self.health = MOB_HEALTH
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rot = 0
        self.speed = choice(MOB_SPEED)
        self.move = False
    
    def avoid_mobs(self):
        # to avoid mobs stacking on each other and have separate positions
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def detect_target(self):
        dist = self.pos - self.game.player.pos
        if dist.length() < DETECT_RADIUS:
            return True
        else:
            return False    

    def update(self):
        if self.detect_target():
            if random() < 0.005:
                choice(self.game.zombie_moan_sounds).play()
            self.rot = (self.game.player.pos - self.pos).angle_to(vec(1,0))
            self.image = pg.transform.rotate(self.game.mob_img , self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vec(1 , 0).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt **2
        self.hit_rect.centerx = self.pos.x 
        collide_with_walls(self , self.game.walls , 'x')  
        self.hit_rect.centery = self.pos.y    
        collide_with_walls(self , self.game.walls , 'y')
        self.rect.center = self.hit_rect.center 
        if self.health <= 0:
            choice(self.game.zombie_hit_sounds).play() 
            self.game.total_zombies -= 1
            self.game.map_img.blit(self.game.splat, self.pos - vec(32,32))
            self.game.killed += 1
            self.kill()

    def healthBar(self):
        if self.health >= 60:
            col = GREEN
        elif self.health >= 30:
            col = YELLOW
        else :
            col = RED
        width = int(self.rect.width * self.health/100)
        self.health_bar = pg.Rect(0 , 0 , width , 7)
        if self.health < 100:
            pg.draw.rect(self.image , col , self.health_bar)                    

class Bullets(pg.sprite.Sprite):

    def __init__(self, game , pos , dir , damage):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites , game.bullets
        pg.sprite.Sprite.__init__(self , self.groups)
        self.game = game
        self.image = game.bullet_images[WEAPONS[game.player.weapon]['bullet_size']]
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.hit_rect = self.rect
        self.rect.center = pos
        self.damage = damage
        # spread = uniform(-GUN_SPREAD , GUN_SPREAD)
        if self.game.player.weapon == 'shotgun':
            self.vel = dir* WEAPONS[game.player.weapon]['bullet_speed'] * uniform(0.9 , 1.1)
        else:    
            self.vel = dir* WEAPONS[game.player.weapon]['bullet_speed']
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.time.get_ticks() - self.spawn_time > WEAPONS[self.game.player.weapon]['bullet_lifetime']:
            self.kill()
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()       
                     
class MuzzleFlash(pg.sprite.Sprite):
    def __init__(self , game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = randint(20,50)
        self.image = pg.transform.scale(choice(game.gun_flashes) , (size,size))
        self.image = pg.transform.rotate(self.image , (self.game.player.rot - 90)% 360)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()
    
    def update(self):
        if pg.time.get_ticks() - self.spawn_time > FLASH_DUR:
            self.kill()

class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        self.groups = game.all_sprites, game.items
        self._layer = ITEM_LAYER
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.type = type
        self.pos = pos
        self.rect.center = pos
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1

    def update(self):
        offset = BOB_RANGE * (self.tween(self.step/BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset*self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1
