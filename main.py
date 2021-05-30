import pygame as pg
import os

from constants import FPS, SCREEN, BG, PLAYER_STATUSES, IDLE_ANIMATION_COOLDOWN, RED, WIDTH, GROUD_LINE
from sprites.characters import Player, Enemy
from secondary import Grenade, ply_bullet_group, enemy_bullet_group, enemy_group, grenade_group, explosions_group
pg.display.set_caption('Shooter')
pjoin = os.path.join
#NUM_IMAGE_FRAMES = 4
#player_image_set = [ pjoin(IMG_FOLDER,'Idle', f'{str(n)}.png') for n in range(NUM_IMAGE_FRAMES)]

def draw_bg():
    SCREEN.fill(BG)
    pg.draw.line(SCREEN, RED, (0,GROUD_LINE), (WIDTH, GROUD_LINE))


pg.mixer.init() # todo reactivate for to enable sounds
pg.init()
clock = pg.time.Clock()


ply = Player(200, 100, ply_bullet_group)
enemy1 = Enemy(400, 400, enemy_bullet_group, flip=True)
enemy_group.add(enemy1)

if __name__ == '__main__':
    run = True
    forward, back, shoot, grenade, grenade_throw = None, None, None, None, None
    counter = 0
    while run:
        clock.tick(FPS)
        draw_bg()
        if shoot:
            ply.shoot()

        ply.update()
        ply.draw()
        if grenade and not grenade_throw and ply.grenades > 0:
            direction = 1 if ply.facing_direction else -1
            grenade = Grenade(ply.rect.centerx + (0.5 * ply.rect.size[0] * direction),
                              ply.rect.top, direction)
            grenade_group.add(grenade)
            ply.grenades -= 1
            grenade_throw = True

        grenade_group.update()
        grenade_group.draw(SCREEN)
        explosions_group.update()
        explosions_group.draw(SCREEN)
        enemy_group.update()
        enemy_group.draw(SCREEN)
        ply.move(forward=forward, back=back)
        enemy1.move(False, False)
        ply_bullet_group.update()
        enemy_bullet_group.update()
        ply_bullet_group.draw(SCREEN)
        enemy_bullet_group.draw(SCREEN)
        # if not counter % IDLE_ANIMATION_COOLDOWN:
        #     ply.imageset.next_image()
        # event handler
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False
                if event.key == pg.K_RIGHT:
                    forward = True
                    # back = False
                if event.key == pg.K_LEFT:
                    back = True
                    # forward = False
                if event.key == pg.K_UP and ply.is_alive and not ply.in_air:
                    ply.jump = True
                if event.key == pg.K_SPACE:
                    shoot = True
                if event.key == pg.K_LALT:
                    grenade = True

            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT:
                    back = False
                if event.key == pg.K_RIGHT:
                    forward = False
                if event.key == pg.K_SPACE:
                    shoot = False
                if event.key == pg.K_LALT:
                    grenade = False
                    grenade_throw = False


        pg.display.update()
    pg.quit()