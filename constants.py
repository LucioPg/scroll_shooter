import os
from utils import get_files_num, get_statuses
import pygame as pg

FPS = 60
WIDTH = 800
HEIGHT = int(WIDTH * 0.8)
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
IMG_FOLDER = 'img'# os.path.join('img','player')
BG = (144, 201, 120)
RED = (144, 0, 0)
PLAYER_STATUSES = get_statuses(os.path.join(IMG_FOLDER, 'player'))
ENEMIES_STATUSES = get_statuses(os.path.join(IMG_FOLDER, 'enemy'))
BULLET_IMG = os.path.join(IMG_FOLDER, 'bullets_and_grenades','bullet.png')
GRENADE_IMG = os.path.join(IMG_FOLDER, 'bullets_and_grenades','grenade.png')
EXPLOSION_STATUSES = get_statuses(os.path.join(IMG_FOLDER, 'explosion'))
IDLE_ANIMATION_COOLDOWN = 90
JUMP_ACTION_COOLDOWN = 40
GRAVITY = 0.981
GROUD_LINE = HEIGHT // 2
SCALE = 3