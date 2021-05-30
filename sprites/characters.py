from functools import wraps
import pygame as pg

from commons import ImageSet, Cooldown
from constants import (SCREEN,
                       GRAVITY,
                       GROUD_LINE,
                       IDLE_ANIMATION_COOLDOWN,
                       JUMP_ACTION_COOLDOWN,
                       PLAYER_STATUSES,
                       ENEMIES_STATUSES)
from secondary import Bullet



class SoldierTemplate(pg.sprite.Sprite):
    # def __init__(self, x, y, scale=3, speed=5, ammo=20, health=100, **kwargs):
    front = True
    back = False

    def dec_cooldown(func):
        def inner(self,*args, **kwargs):
            cooldown = kwargs.get('cooldown', None)
            if cooldown is None:
                raise Exception("missing cooldown arg")
            if pg.time.get_ticks() - self.update_time > cooldown:
                self.update_time = pg.time.get_ticks()
                func(self, cooldown)
        return inner

    def __init__(self,char_type, bullet_group, speed=5, ammo=20, health=100, **kwargs):
        pg.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.ammo = ammo
        self.shoot_cooldown = 0
        self.bullet_group = bullet_group
        self.health = self.max_health = health
        self.speed = speed
        self.up_speed = -15 # negative to go up
        self.vel_y = 0
        self.is_alive = True
        self.in_air = self.jump = self.flip = False
        self.imageset = self.image = self.rect = None
        self.facing_direction = self.front
        self.update_time = pg.time.get_ticks()
        # self.imageset, self.image, self.rect = self.init_imageset(x, y, scale, statuses)
        for arg_name, val in kwargs.items():
            setattr(self, arg_name, val)



    def init_imageset(self, x, y, scale, statuses, char_type):
        imageset = ImageSet(self, x, y, scale, statuses=statuses, char_type=char_type, first_status=statuses[0])
        image, rect = self.init_image_rect(imageset)
        return imageset, image, rect

    @staticmethod
    def init_image_rect(imageset):
        return imageset.image, imageset.rect

    def update_image(self):
        self.image, self.rect = self.imageset.image, self.imageset.rect

    def move(self, forward=None, back=None):
        x, y = 0, 0
        if forward != back:
            if forward:
                self.flip = False
                x += self.speed
                self.facing_direction = self.front
            if back:
                self.flip = True
                x -= self.speed
                self.facing_direction = self.back
        # else:
        #     self.update_status('Idle')

        self.rect.x += x

        if self.jump and self.in_air == False:
            # if self.in_air:
            self.vel_y = self.up_speed
            self.jump = False
        self.vel_y += GRAVITY
        y += self.vel_y
        # if self.vel_y >= 0:
        #     self.in_air = False
        y = self.check_ground_collision(y)
        self.check_status(back, forward)


        # if self.in_air:
        #     self.jump = False

        self.rect.y += y


    # @dec_cooldown
    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            direction = 1 if self.facing_direction else -1
            bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * direction), self.rect.centery,
                            direction, self)
            self.bullet_group.add(bullet)
            # reduce ammo
            self.ammo -= 1

    def update(self, cooldown=IDLE_ANIMATION_COOLDOWN) -> None:
        self.update_animation(cooldown=IDLE_ANIMATION_COOLDOWN)
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.health <= 0:
            self.is_alive = False

    @dec_cooldown
    def update_animation(self, cooldown=IDLE_ANIMATION_COOLDOWN):
        # update animation
        one_round = not self.is_alive
        self.imageset.next_image(one_round=one_round)

    def check_status(self, back, forward):
        if not self.in_air and self.is_alive:
            if back == forward or (not back and not forward):
                self.set_status('Idle')
            else:
                self.set_status('Run')
        elif self.in_air and self.is_alive:
            self.set_status('Jump')
        else:
            self.set_status('Death')


    def check_ground_collision(self, dy):
        if self.rect.bottom + dy > GROUD_LINE:
            dy = GROUD_LINE - self.rect.bottom
            self.in_air = False
        else:
            self.in_air = True

        return dy

    def draw(self):
        if self.char_type == 'enemy':
            print()
        SCREEN.blit(pg.transform.flip(self.image, self.flip, False), self.rect)

    def status(self):
        return self.imageset.current_status

    def set_status(self, status):
        self.imageset.update_status(status)

    def __str__(self):
        return self.char_type

    def __repr__(self):
        return self.char_type
    # def decorator_status_check(self, *args, **kwargs):
    #     @wraps
    #     def inner(*args, **kwargs):




class Player(SoldierTemplate):
    def __init__(self, x, y, bullet_group, scale=3, speed=5, ammo=20, health=100, grenades=5, **kwargs):
        self.char_type = 'player'
        self.grenades = grenades
        super(Player, self).__init__(self.char_type, bullet_group, speed=5, ammo=20, health=100, **kwargs)
        statuses = PLAYER_STATUSES
        self.imageset, self.image, self.rect = self.init_imageset(x, y, scale, statuses, self.char_type)


class Enemy(SoldierTemplate):
    def __init__(self, x, y, bullet_group, scale=3, speed=5, ammo=20, health=100, **kwargs):
        self.flip = kwargs.get('flip', False)
        self.char_type = 'enemy'
        super(Enemy, self).__init__(self.char_type, bullet_group, speed=5, ammo=20, health=100, flip=self.flip)
        statuses = ENEMIES_STATUSES

        self.imageset, self.image, self.rect = self.init_imageset(x, y, scale, statuses, self.char_type)


if __name__ == '__main__':
    a = Player(200,200)
    print(a)
    print()