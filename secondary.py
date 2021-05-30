import pygame as pg
from constants import IDLE_ANIMATION_COOLDOWN, BULLET_IMG, GRENADE_IMG, WIDTH, GRAVITY, GROUD_LINE, EXPLOSION_STATUSES, SCALE
from commons import ImageSet, Cooldown

ply_bullet_group = pg.sprite.Group()
enemy_bullet_group = pg.sprite.Group()
enemy_group = pg.sprite.Group()
grenade_group = pg.sprite.Group()
explosions_group = pg.sprite.Group()

class Bullet(pg.sprite.Sprite):

    def __init__(self, x, y, direction, player, *args, **kwargs):
        pg.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = pg.image.load(BULLET_IMG).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.player = player

    def update(self, *args, **kwargs) -> None:
        # move bullet
        self.rect.x += (self.direction * self.speed)
        # check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()

        # check collision with characters
        if pg.sprite.spritecollide(self.player, enemy_bullet_group, False):
            if self.player.alive:
                self.player.health -= 5
                self.kill()

        for enemy in enemy_group:
            if pg.sprite.spritecollide(enemy, ply_bullet_group, False):
                if enemy.alive:
                    enemy.health -= 25
                    print(enemy.health)
                    self.kill()


class Grenade(pg.sprite.Sprite):

    def __init__(self, x, y, direction):
        pg.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -11
        self.speed = 7
        self.image = pg.image.load(GRENADE_IMG).convert_alpha()
        self.x = x
        self.y = y
        self.direction = direction
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.timer -= 1
        if self.timer == 0:
            explosion = Explosion(self.rect.x, self.rect.y)
            explosions_group.add(explosion)
            self.kill()
        dx = dy = 0
        self.vel_y += GRAVITY
        dx += self.speed * self.direction
        dy = self.vel_y
        # check collision with floor
        if self.rect.bottom + dy > GROUD_LINE:
            dy = GROUD_LINE - self.rect.bottom
            self.speed = 0

        # check collision with walls
        if self.rect.left + dx < 0 or self.rect.right + dx > WIDTH:
            self.direction *= -1
            dx = self.direction * self.speed
        self.rect.x += dx
        self.rect.y += dy

class Explosion(pg.sprite.Sprite):


    def dec_cooldown(func):
        def inner(self,*args, **kwargs):
            cooldown = kwargs.get('cooldown', None)
            if cooldown is None:
                raise Exception("missing cooldown arg")
            if pg.time.get_ticks() - self.update_time > cooldown:
                self.update_time = pg.time.get_ticks()
                func(self, cooldown)
        return inner

    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.imageset, self.image, self.rect = self.init_imageset(x,y, SCALE, EXPLOSION_STATUSES, char_type='explosion')
        self.imageset.last_frame_signal.connect(self.autokill)
        self.update_time = pg.time.get_ticks()


    def autokill(self):
        self.kill()

    @dec_cooldown
    def update_animation(self, cooldown=IDLE_ANIMATION_COOLDOWN):
        # update animation
        one_round = True
        self.imageset.next_image(one_round=one_round)


    def init_imageset(self, x, y, scale, statuses, char_type):
        imageset = ImageSet(self, x, y, scale, statuses=statuses, char_type=char_type, first_status=statuses[0])
        image, rect = self.init_image_rect(imageset)
        return imageset, image, rect

    @staticmethod
    def init_image_rect(imageset):
        return imageset.image, imageset.rect

    def update_image(self):
        self.image, self.rect = self.imageset.image, self.imageset.rect

    def update(self, *args, **kwargs) -> None:
        self.update_animation(cooldown=IDLE_ANIMATION_COOLDOWN)