from math import fabs, trunc
import pygame as pg
vec = pg.math.Vector2

# colors (R, G , B)
WHITE = (255 , 255 , 255)
BLACK = (0 , 0 , 0)
DARKGREY = (40 , 40 , 40)
LIGHTGREY = (100 , 100 , 100)
GREEN = (0 , 255 , 0)
RED = (255 , 0 , 0)
YELLOW = (255 , 255 , 0)
BROWN = (186, 55, 5)

# game settings
WIDTH = 1024
HEIGHT = 768
FPS = 60
TITLE = "ZOMBIE SHOOTER"
BGCOLOR = BROWN

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player Settings 
PLAYER_SPEED = 5*TILESIZE
PLAYER_ROT_SPEED = 256
PLAYER_HIT_RECT = pg.Rect(0, 0, int(TILESIZE / 1.5), int(TILESIZE / 1.5))
GUN_OFFSET = vec(30 , 10)
BAR_LENGTH = 400
PLAYER_HEALTH = 1000
GUN = {}
GUN['pistol'] = {
    'equipped' : True,
    'ammo': 149
}
GUN['shotgun'] = {
    'equipped' : False,
    'ammo': 0
}
GUN['rifle'] = {
    'equipped' : False,
    'ammo': 0
}

# Zombie Settings
MOB_SPEED = [ 3.45*TILESIZE , 3.5* TILESIZE , 3.25*TILESIZE , 3.75*TILESIZE , 3.85 * TILESIZE ,4*TILESIZE , 4.05*TILESIZE , 4.15*TILESIZE]
MOB_HIT_RECT = pg.Rect(0, 0, int(TILESIZE / 1.5), int(TILESIZE / 1.5))
MOB_HEALTH = 100
MOB_DAMAGE = 150
MOB_KNOCKBACK = 20
AVOID_RADIUS = 50
DETECT_RADIUS = 9*TILESIZE

# Weapon Setting
BULLET_SPEED = 500
WEAPONS ={}
WEAPONS['pistol'] = {
    'bullet_speed': 450,
    'bullet_lifetime': 1000,
    'rate': 350,
    'spread': 5,
    'kickback': 200,
    'bullet_damage':21,
    'bullet_size': 'lg',
    'bullet_count': 1,
    'clip': 149
}

WEAPONS['shotgun'] = {
    'bullet_speed': 350,
    'bullet_lifetime': 500,
    'rate': 900,
    'spread': 30,
    'kickback': 400,
    'bullet_damage':6,
    'bullet_size': 'sm',
    'bullet_count': 12,
    'clip': 30
}

WEAPONS['rifle'] = {
    'bullet_speed': 450,
    'bullet_lifetime': 1000,
    'rate': 120,
    'spread': 6,
    'kickback': 110,
    'bullet_damage':15,
    'bullet_size': 'md',
    'bullet_count': 1,
    'clip': 90
}

#Effects
MUZZLE_FLASH = ['muzzle_01.png' , 'muzzle_02.png' , 'muzzle_03.png', 'muzzle_04.png' , 'muzzle_05.png' ]
FLASH_DUR = 20
DAMAGE_ALPHA = [i for i in range(0 , 255, 50)]
LIGHT_RADIUS = (600,600)
LIGHT_MASK = "light_350_med.png"
NIGHT_COLOR = (70,70,70)

# images
FACE_LOGO = 'player_face.png'
PLAYER_IMG = 'player.png'
WALL_IMG = 'wall.png'
ZOMBIE_IMG = 'zombie.png'
BULLET_IMG = 'bullet.png'
AMMO_IMG = 'ammo.png'
HAZARD_IMG = 'hazard.png'
GAME_OVER = 'rip.jpg'
SURVIVED_IMAGE = 'won.jpg'

# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEM_LAYER = 1

# Items
ITEM_IMAGES = {
    'health': 'medkit.png',
    'shotgun': 'shotgun.png',
    'rifle': 'rifle.png'
}
HEAL_AMOUNT = 450
BOB_RANGE = 15
BOB_SPEED = 0.4

# Sounds
BG_MUSIC = 'espionage.ogg'
PLAYER_HIT_SOUND = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav']
ZOMBIE_MOAN_SOUND = ['brains2.wav', 'brains3.wav', 'zombie-roar-1.wav' , 'zombie-roar-2.wav', 'zombie-roar-3.wav',
                    'zombie-roar-4.wav' , 'zombie-roar-5.wav', 'zombie-roar-6.wav', 'zombie-roar-7.wav']
ZOMBIE_HIT_SOUND = ['splat-15.wav']
WEAPON_SOUNDS = {}
WEAPON_SOUNDS['pistol'] = ['pistol.wav'] 
WEAPON_SOUNDS['rifle'] = ['pistol.wav'] 
WEAPON_SOUNDS['shotgun'] = ['shotgun.wav'] 
EFFECTS_SOUND = {'level_start': 'level_start.wav',
                'health_up': 'health_pack.wav',
                'gun_pickup': 'gun_pickup.wav',
                'gun_switch': 'gun_switch.mp3',
                'empty': 'empty.wav'}
