import os

import pygame as pg
from functools import wraps
from utils import get_files_num
from collections import OrderedDict

pjoin = os.path.join


class Cooldown:
    @staticmethod
    def dec_cooldown(cls, func, cooldown):
        @wraps
        def inner():
            if pg.time.get_ticks() - cls.update_time > cooldown:
                cls.update_time = pg.time.get_ticks()
                func()

        return inner

class IteratorAnimation:
    def __init__(self, animation):
        self._animation = animation
        self._generator = (status for status in animation.statuses)
    def __next__(self):
        """Returns the next status"""
        return next(self._generator)

class Animations:
    # base_folder = pjoin('..','img')
    base_folder = 'img'
    ext = '.png'
    def __init__(self, char, statuses):
        self.char = char # can be player or enemy
        self.statuses = statuses
        self.animations = self.set_animations()
        self._reset_animations = self.animations.copy()
        self._index = 0
        self.folders = []
        self.set_animations()

    def set_animations(self):
        animations = OrderedDict()
        for status in self.statuses:
            folder = pjoin(self.base_folder, self.char, status)
            if not os.path.exists(folder):
                raise Exception(f"The path {folder} does not exist")
            frames = get_files_num(folder)
            animations[status] = [ pjoin(folder, f'{str(n)}{self.ext}') for n in range(frames)]
        return animations

    def is_last_frame(self, status):
        return self.animations[status][0] == self._reset_animations[status][-1]

    def reset(self):
        self.animations = self._reset_animations.copy()

    def __iter__(self):
        return IteratorAnimation(self)

    def __getitem__(self, index):
        return self.animations.get(index, '')

    def __setitem__(self, key, value):
        self.animations[key] = value



class ImageSet:
    def __init__(self, sprite, x, y, scale, char_type, statuses, first_status:str):
        self.sprite = sprite
        if first_status in statuses:
            self.current_status = first_status
        else:
            if statuses:
                self.current_status = statuses[0]
            else:
                raise Exception(f'statuses list can not be empty')
        self.animations = Animations(char_type, statuses)
        self.scale = scale
        img = pg.image.load(self.current_image_file())
        self._image = pg.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.last_frame_signal = SignalLastFrame()


    def update_status(self, status):
        if status in self.animations:
            if self.current_status != status:
                self.animations.reset()
                self.current_status = status

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, path):
        img = pg.image.load(path)
        self._image = pg.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
        self.sprite.update_image()

    def rotate_image_set(self, step=1, rotation_direction=True):
        if self.animations and  len(self.animations[self.current_status]) > step:
            if not rotation_direction:
                step *= - 1
            self.animations[self.current_status] = self.animations[self.current_status][step:] + self.animations[self.current_status][:step]
        return self.animations[self.current_status]

    def next_image(self, rotation_direction=True, one_round=False):
        if not one_round:
            self.rotate_image_set(rotation_direction=rotation_direction)
        else:
            if not self.animations.is_last_frame(self.current_status):
                self.rotate_image_set(rotation_direction=rotation_direction)
            else:
                self.last_frame_signal.trigger()
        self.image = self.current_image_file()
        return self.image

    def current_image_file(self):
        if not self.animations or not os.path.exists(self.animations[self.current_status][0]):
            raise Exception("The image set can not be empty")
        return self.animations[self.current_status][0]



class SignalLastFrame:
    name = 'last_frame'
    __connections = []


    def connect(self, slot):
        self.__connections.append(slot)

    def trigger(self, *args, **kwargs):
        for slot in self.__connections:
            slot(*args, **kwargs)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
