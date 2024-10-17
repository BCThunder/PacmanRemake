import pygame as pg
from pygame.sprite import Sprite
from timer import Timer

class Ghost(Sprite):
    blinky = ['blinky1.png', 'blinky2.png']
    blinky_imgs = [pg.image.load(f"pacman_imgs/{name}") for name in blinky]
    blinky_anim = [pg.transform.scale(x,  (32, 32)) for x in blinky_imgs]

    inky = ['inky1.png', 'inky2.png']
    inky_imgs = [pg.image.load(f"pacman_imgs/{name}") for name in inky]
    inky_anim = [pg.transform.scale(x, (32, 32)) for x in inky_imgs]

    pinky = ['pinky1.png', 'pinky2.png']
    pinky_imgs = [pg.image.load(f"pacman_imgs/{name}") for name in pinky]
    pinky_anim = [pg.transform.scale(x, (32, 32)) for x in pinky_imgs]

    clyde = ['clyde1.png', 'clyde2.png']
    clyde_imgs= [pg.image.load(f"pacman_imgs/{name}") for name in clyde]
    clyde_anim = [pg.transform.scale(x, (32, 32)) for x in clyde_imgs]

    ghost_anim = [blinky_anim, inky_anim, pinky_anim, clyde_anim]
    ghost_names = ['blinky', 'inky', 'pinky', 'clyde']

    eyes = ['eyes1.png', 'eyes2.png']
    eyes_imgs = [pg.image.load(f"pacman_imgs/{name}") for name in eyes]
    eyes_anim = [pg.transform.scale(x, (32, 32)) for x in eyes_imgs]

    run = ['run1.png', 'run2.png']
    run_imgs= [pg.image.load(f"pacman_imgs/{name}") for name in run]
    run_anim = [pg.transform.scale(x, (32, 32)) for x in run_imgs]

    def __init__(self, game, ghost_num = 0):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.screen_height = self.settings.screen_height
        self.screen_width = self.settings.screen_width
        self.player = game.player
        self.map = game.map.map

        self.regtimer = Timer(Ghost.ghost_anim[ghost_num], start_index = 0, delta = 6)
        self.runtimer = Timer(Ghost.run_anim, start_index = 0, delta = 6)
        self.eyestimer = Timer(Ghost.eyes_anim, start_index = 0, delta = 6)
        self.timer = self.regtimer
        self.image = Ghost.ghost_anim[0][0]
        self.name = Ghost.ghost_names[ghost_num]

        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.center_x = self.rect.centerx
        self.center_y = self.rect.centery

        self.speed = self.settings.ghost_speed
        self.direction = 0
        self.allowed_direction = [False, False, False, False]
        self.is_dying = False
        self.eaten = False
        self.in_box = True
        self.in_tunnel = False
        self.points = game.settings.ghost_points

    def clamp(self):
        self.center_x = self.rect.centerx
        self.center_y = self.rect.centery
        self.target_x = self.player.rect.x
        self.target_y = self.player.rect.y
        num1 = ((self.screen_height - 50) // 32)
        num2 = (self.screen_width // 30)
        buffer = 13
        self.allowed_direction = [False, False, False, False]

        if (self.center_y // num1) == 15 and ((self.center_x // num2) <= 6 or (self.center_x // num2) >= 23):
            self.in_tunnel = True
            self.allowed_direction[self.direction] = True

            if self.rect.centerx < -5:
                self.rect.centerx = 716
            elif self.rect.centerx > 905:
                self.rect.centerx = -5
        else:
            self.in_tunnel = False

        if self.in_tunnel is False:
            if 280 < self.rect.x < 430 and 286 < self.rect.y < 374:
                self.in_box = True
                if self.eaten:
                    self.is_dying = False
            else:
                self.in_box = False

            if 0 < self.center_x // 30 < 29:
                if self.map[(self.center_y - buffer) // num1][self.center_x // num2] == 9:
                    self.allowed_direction[2] = True

                if self.map[self.center_y // num1][(self.center_x - buffer) // num2] < 3 \
                    or (self.map[self.center_y // num1][(self.center_x - buffer) // num2] == 9 and (
                        self.in_box or self.is_dying)):
                    self.allowed_direction[1] = True

                if self.map[self.center_y // num1][(self.center_x + buffer) // num2] < 3 \
                    or (self.map[self.center_y // num1][(self.center_x + buffer) // num2] == 9 and (
                        self.in_box or self.is_dying)):
                    self.allowed_direction[0] = True

                if self.map[(self.center_y + buffer) // num1][self.center_x // num2] < 3 \
                    or (self.map[(self.center_y + buffer) // num1][self.center_x // num2] == 9 and (
                        self.in_box or self.is_dying)):
                    self.allowed_direction[3] = True

                if self.map[(self.center_y - buffer) // num1][self.center_x // num2] < 3 \
                    or (self.map[(self.center_y - buffer) // num1][self.center_x // num2] == 9 and (
                        self.in_box or self.is_dying)):
                    self.allowed_direction[2] = True

                if self.direction == 2 or self.direction == 3:
                    if 9 <= self.center_x % num2 <= 15:
                        if self.map[(self.center_y + buffer) // num1][self.center_x // num2] < 3 \
                            or (self.map[(self.center_y + buffer) // num1][self.center_x // num2] == 9 and (
                                self.in_box or self.is_dying)):
                            self.allowed_direction[3] = True

                        if self.map[(self.center_y - buffer) // num1][self.center_x // num2] < 3 \
                            or (self.map[(self.center_y - buffer) // num1][self.center_x // num2] == 9 and (
                                self.in_box or self.is_dying)):
                            self.allowed_direction[2] = True

                    if 9 <= self.center_y % num1 <= 15:
                        if self.map[self.center_y // num1][(self.center_x - num2) // num2] < 3 \
                            or (self.map[self.center_y // num1][(self.center_x - num2) // num2] == 9 and (
                                self.in_box or self.is_dying)):
                            self.allowed_direction[1] = True

                        if self.map[self.center_y // num1][(self.center_x + num2) // num2] < 3 \
                            or (self.map[self.center_y // num1][(self.center_x + num2) // num2] == 9 and (
                                self.in_box or self.is_dying)):
                            self.allowed_direction[0] = True

                if self.direction == 0 or self.direction == 1:
                    if 9 <= self.center_x % num2 <= 15:
                        if self.map[(self.center_y + buffer) // num1][self.center_x // num2] < 3 \
                            or (self.map[(self.center_y + buffer) // num1][self.center_x // num2] == 9 and (
                                self.in_box or self.is_dying)):
                            self.allowed_direction[3] = True

                        if self.map[(self.center_y - buffer) // num1][self.center_x // num2] < 3 \
                            or (self.map[(self.center_y - buffer) // num1][self.center_x // num2] == 9 and (
                                self.in_box or self.is_dying)):
                            self.allowed_direction[2] = True

                    if 9 <= self.center_y % num1 <= 15:
                        if self.map[self.center_y // num1][(self.center_x - buffer) // num2] < 3 \
                            or (self.map[self.center_y // num1][(self.center_x - buffer) // num2] == 9 and (
                                self.in_box or self.is_dying)):
                            self.allowed_direction[1] = True

                        if self.map[self.center_y // num1][(self.center_x + buffer) // num2] < 3 \
                            or (self.map[self.center_y // num1][(self.center_x + buffer) // num2] == 9 and (
                                self.in_box or self.is_dying)):
                            self.allowed_direction[0] = True

            else:
                self.allowed_direction[0] = True
                self.allowed_direction[1] = True
                
    def get_target(self):
        player_x = self.player.rect.x
        player_y = self.player.rect.y
        box_target = (334, 324)      # x, y coords of the box
        box_out = (335, 80)          # x, y coords just outside the box

        if player_x < 360:
            run_x = self.screen_width
        else:
            run_x = 0
        if player_y < 360:
            run_y = self.screen_height - 40
        else:
            run_y = 0

        if self.in_box:
            self.target_x, self.target_y = box_out

        elif self.eaten:
            self.target_x, self.target_y = box_target

        elif self.player.power_up and not self.eaten:
                if self.name == 'blinky':
                        self.target_x, self.target_y = run_x, run_y
                
                elif self.name == 'inky':
                    self.target_x, self.target_y = run_x, player_y
                
                elif self.name == 'pinky':
                    self.target_x, self.target_y = player_x, run_y

                elif self.name == 'clyde':
                    self.target_x, self.target_y = (360, 360)

        else:
            self.target_x, self.target_y = player_x, player_y         

    def move_clyde(self):
        # r, l, u, d
        if self.direction == 0:
            if self.target_x > self.rect.x and self.allowed_direction[0]:
                self.rect.x += self.speed
            elif not self.allowed_direction[0]:
                if self.target_y > self.rect.y and self.allowed_direction[3]:
                    self.direction = 3
                    self.rect.y += self.speed
                elif self.target_y < self.rect.y and self.allowed_direction[2]:
                    self.direction = 2
                    self.rect.y -= self.speed
                elif self.target_x < self.rect.x and self.allowed_direction[1]:
                    self.direction = 1
                    self.rect.x -= self.speed
                elif self.allowed_direction[3]:
                    self.direction = 3
                    self.rect.y += self.speed
                elif self.allowed_direction[2]:
                    self.direction = 2
                    self.rect.y -= self.speed
                elif self.allowed_direction[1]:
                    self.direction = 1
                    self.rect.x -= self.speed
            elif self.allowed_direction[0]:
                if self.target_y > self.rect.y and self.allowed_direction[3]:
                    self.direction = 3
                    self.rect.y += self.speed
                if self.target_y < self.rect.y and self.allowed_direction[2]:
                    self.direction = 2
                    self.rect.y -= self.speed
                else:
                    self.rect.x += self.speed

        elif self.direction == 1:
            if self.target_y > self.rect.y and self.allowed_direction[3]:
                self.direction = 3
            elif self.target_x < self.rect.x and self.allowed_direction[1]:
                self.rect.x -= self.speed
            elif not self.allowed_direction[1]:
                if self.target_y > self.rect.y and self.allowed_direction[3]:
                    self.direction = 3
                    self.rect.y += self.speed
                elif self.target_y < self.rect.y and self.allowed_direction[2]:
                    self.direction = 2
                    self.rect.y -= self.speed
                elif self.target_x > self.rect.x and self.allowed_direction[0]:
                    self.direction = 0
                    self.rect.x += self.speed
                elif self.allowed_direction[3]:
                    self.direction = 3
                    self.rect.y += self.speed
                elif self.allowed_direction[2]:
                    self.direction = 2
                    self.rect.y -= self.speed
                elif self.allowed_direction[0]:
                    self.direction = 0
                    self.rect.x += self.speed
            elif self.allowed_direction[1]:
                if self.target_y > self.rect.y and self.allowed_direction[3]:
                    self.direction = 3
                    self.rect.y += self.speed
                if self.target_y < self.rect.y and self.allowed_direction[2]:
                    self.direction = 2
                    self.rect.y -= self.speed
                else:
                    self.rect.x -= self.speed

        elif self.direction == 2:
            if self.in_box and self.target_y < self.rect.y and self.allowed_direction[2]:
                self.direction = 2
                self.rect.y -= self.speed
            elif self.target_x < self.rect.x and self.allowed_direction[1]:
                self.direction = 1
                self.rect.x -= self.speed 
            elif self.target_y < self.rect.y and self.allowed_direction[2]:
                self.direction = 2
                self.rect.y -= self.speed
            elif not self.allowed_direction[2]:
                if self.target_x > self.rect.x and self.allowed_direction[0]:
                    self.direction = 0
                    self.rect.x += self.speed
                elif self.target_x < self.rect.x and self.allowed_direction[1]:
                    self.direction = 1
                    self.rect.x -= self.speed
                elif self.target_y > self.rect.y and self.allowed_direction[3]:
                    self.direction = 3
                    self.rect.y += self.speed
                elif self.allowed_direction[1]:
                    self.direction = 1
                    self.rect.x -= self.speed
                elif self.allowed_direction[3]:
                    self.direction = 3
                    self.rect.y += self.speed
                elif self.allowed_direction[0]:
                    self.direction = 0
                    self.rect.x += self.speed
            elif self.allowed_direction[2]:
                if self.in_box:
                    self.rect.y -= self.speed
                elif self.target_x > self.rect.x and self.allowed_direction[0]:
                    self.direction = 0
                    self.rect.x += self.speed
                elif self.target_x < self.rect.x and self.allowed_direction[1]:
                    self.direction = 1
                    self.rect.x -= self.speed
                else:
                    self.rect.y -= self.speed

        elif self.direction == 3:
            if self.target_y > self.rect.y and self.allowed_direction[3]:
                self.rect.y += self.speed 
            elif not self.allowed_direction[3]:
                if self.target_x > self.rect.x and self.allowed_direction[0]:
                    self.direction = 0
                    self.rect.x += self.speed 
                elif self.target_x < self.rect.x and self.allowed_direction[1]:
                    self.direction = 1
                    self.rect.x -= self.speed
                elif self.target_y < self.rect.y and self.allowed_direction[2]:
                    self.direction = 2
                    self.rect.y -= self.speed
                elif self.allowed_direction[2]:
                    self.direction = 2
                    self.rect.y -= self.speed
                elif self.allowed_direction[1]:
                    self.direction = 1 
                    self.rect.x -= self.speed
                elif self.allowed_direction[0]:
                    self.direction = 0
                    self.rect.x += self.speed
            elif self.allowed_direction[3]:
                if self.target_x > self.rect.x and self.allowed_direction[0]:
                    self.direction = 0
                    self.rect.x += self.speed
                elif self.target_x < self.rect.x and self.allowed_direction[1]:
                    self.direction = 1
                    self.rect.x -= self.speed
                else:
                    self.rect.y += self.speed 
    
    def move_blinky(self):
        # r, l, u, d
        if self.direction == 0:
            if self.target_x > self.rect.x and self.allowed_direction[0]:
                self.rect.x += self.speed
            elif not self.allowed_direction[0]:
                if self.target_y > self.rect.y and self.allowed_direction[3]:
                    self.direction = 3
                    self.rect.y += self.speed
                elif self.target_y < self.rect.y and self.allowed_direction[2]:
                    self.direction = 2
                    self.rect.y -= self.speed
                elif self.target_x < self.rect.x and self.allowed_direction[1]:
                    self.direction = 1
                    self.rect.x -= self.speed
                elif self.allowed_direction[3]:
                    self.direction = 3
                    self.rect.y += self.speed
                elif self.allowed_direction[2]:
                    self.direction = 2
                    self.rect.y -= self.speed
                elif self.allowed_direction[1]:
                    self.direction = 1
                    self.rect.x -= self.speed
            elif self.allowed_direction[0]:
                self.rect.x += self.speed

        elif self.direction == 1:
            if self.target_x < self.rect.x and self.allowed_direction[1]:
                self.rect.x -= self.speed
            elif not self.allowed_direction[1]:
                if self.target_y > self.rect.y and self.allowed_direction[3]:
                    self.direction = 3
                    self.rect.y += self.speed
                elif self.target_y < self.rect.y and self.allowed_direction[2]:
                    self.direction = 2
                    self.rect.y -= self.speed
                elif self.target_x > self.rect.x and self.allowed_direction[0]:
                    self.direction = 0
                    self.rect.x += self.speed
                elif self.allowed_direction[3]:
                    self.direction = 3
                    self.rect.y += self.speed
                elif self.allowed_direction[2]:
                    self.direction = 2
                    self.rect.y -= self.speed
                elif self.allowed_direction[0]:
                    self.direction = 0
                    self.rect.x += self.speed
            elif self.allowed_direction[1]:
                self.rect.x -= self.speed

        elif self.direction == 2:
            if self.target_y < self.rect.y and self.allowed_direction[2]:
                self.direction = 2
                self.rect.y -= self.speed
            elif not self.allowed_direction[2]:
                if self.target_x > self.rect.x and self.allowed_direction[0]:
                    self.direction = 0
                    self.rect.x += self.speed
                elif self.target_x < self.rect.x and self.allowed_direction[1]:
                    self.direction = 1
                    self.rect.x -= self.speed
                elif self.target_y > self.rect.y and self.allowed_direction[3]:
                    self.direction = 3
                    self.rect.y += self.speed
                elif self.allowed_direction[3]:
                    self.direction = 3
                    self.rect.y += self.speed
                elif self.allowed_direction[0]:
                    self.direction = 0
                    self.rect.x += self.speed
                elif self.allowed_direction[1]:
                    self.direction = 1
                    self.rect.x -= self.speed
            elif self.allowed_direction[2]:
                self.rect.y -= self.speed

        elif self.direction == 3:
            if self.target_y > self.rect.y and self.allowed_direction[3]:
                self.rect.y += self.speed 
            elif not self.allowed_direction[3]:
                if self.target_x > self.rect.x and self.allowed_direction[0]:
                    self.direction = 0
                    self.rect.x += self.speed 
                elif self.target_x < self.rect.x and self.allowed_direction[1]:
                    self.direction = 1
                    self.rect.x -= self.speed
                elif self.target_y < self.rect.y and self.allowed_direction[2]:
                    self.direction = 2
                    self.rect.y -= self.speed
                elif self.allowed_direction[2]:
                    self.direction = 2
                    self.rect.y -= self.speed
                elif self.allowed_direction[0]:
                    self.direction = 0
                    self.rect.x += self.speed
                elif self.allowed_direction[1]:
                    self.direction = 1 
                    self.rect.x -= self.speed
            elif self.allowed_direction[3]:self.rect.y += self.speed 

    def move_inky(self):
        # 0 = right, 1 = left, 2 = up, 3 = down
        if self.direction == 0:
            if self.target_x > self.rect.x and self.allowed_direction[0]:
                self.rect.x += self.speed
            elif not self.allowed_direction[0]:
                if self.target_y > self.rect.y and self.allowed_direction[3]:
                    self.direction = 3
                    self.rect.y += self.speed
                elif self.target_y < self.rect.y and self.allowed_direction[2]:
                    self.direction = 2
                    self.rect.y -= self.speed
                elif self.target_x < self.rect.x and self.allowed_direction[1]:
                    self.direction = 1
                    self.rect.x -= self.speed
                elif self.allowed_direction[3]:
                    self.direction = 3
                    self.rect.y += self.speed
                elif self.allowed_direction[2]:
                    self.direction = 2
                    self.rect.y -= self.speed
                elif self.allowed_direction[1]:
                    self.direction = 1
                    self.rect.x -= self.speed
            elif self.allowed_direction[0]:
                if self.target_y > self.rect.y and self.allowed_direction[3]:
                    self.direction = 3
                    self.rect.y += self.speed
                if self.target_y < self.rect.y and self.allowed_direction[2]:
                    self.direction = 2
                    self.rect.y -= self.speed
                else:
                    self.rect.x += self.speed

        elif self.direction == 1:
            if self.target_y > self.rect.y and self.allowed_direction[3]:
                self.direction = 3
            elif self.target_x < self.rect.x and self.allowed_direction[1]:
                self.rect.x -= self.speed
            elif not self.allowed_direction[1]:
                if self.target_y > self.rect.y and self.allowed_direction[3]:
                    self.direction = 3
                    self.rect.y += self.speed
                elif self.target_y < self.rect.y and self.allowed_direction[2]:
                    self.direction = 2
                    self.rect.y -= self.speed
                elif self.target_x > self.rect.x and self.allowed_direction[0]:
                    self.direction = 0
                    self.rect.x += self.speed
                elif self.allowed_direction[3]:
                    self.direction = 3
                    self.rect.y += self.speed
                elif self.allowed_direction[2]:
                    self.direction = 2
                    self.rect.y -= self.speed
                elif self.allowed_direction[0]:
                    self.direction = 0
                    self.rect.x += self.speed
            elif self.allowed_direction[1]:
                if self.target_y > self.rect.y and self.allowed_direction[3]:
                    self.direction = 3
                    self.rect.y += self.speed
                if self.target_y < self.rect.y and self.allowed_direction[2]:
                    self.direction = 2
                    self.rect.y -= self.speed
                else:
                    self.rect.x -= self.speed

        elif self.direction == 2:
            if self.target_y < self.rect.y and self.allowed_direction[2]:
                self.direction = 2
                self.rect.y -= self.speed
            elif not self.allowed_direction[2]:
                if self.target_x > self.rect.x and self.allowed_direction[0]:
                    self.direction = 0
                    self.rect.x += self.speed
                elif self.target_x < self.rect.x and self.allowed_direction[1]:
                    self.direction = 1
                    self.rect.x -= self.speed
                elif self.target_y > self.rect.y and self.allowed_direction[3]:
                    self.direction = 3
                    self.rect.y += self.speed
                elif self.allowed_direction[1]:
                    self.direction = 1
                    self.rect.x -= self.speed
                elif self.allowed_direction[3]:
                    self.direction = 3
                    self.rect.y += self.speed
                elif self.allowed_direction[0]:
                    self.direction = 0
                    self.rect.x += self.speed
            elif self.allowed_direction[2]:
                self.rect.y -= self.speed

        elif self.direction == 3:
            if self.target_y > self.rect.y and self.allowed_direction[3]:
                self.rect.y += self.speed 
            elif not self.allowed_direction[3]:
                if self.target_x > self.rect.x and self.allowed_direction[0]:
                    self.direction = 0
                    self.rect.x += self.speed 
                elif self.target_x < self.rect.x and self.allowed_direction[1]:
                    self.direction = 1
                    self.rect.x -= self.speed
                elif self.target_y < self.rect.y and self.allowed_direction[2]:
                    self.direction = 2
                    self.rect.y -= self.speed
                elif self.allowed_direction[2]:
                    self.direction = 2
                    self.rect.y -= self.speed
                elif self.allowed_direction[1]:
                    self.direction = 1 
                    self.rect.x -= self.speed
                elif self.allowed_direction[0]:
                    self.direction = 0
                    self.rect.x += self.speed
            elif self.allowed_direction[3]:self.rect.y += self.speed

    def move_pinky(self):
        # 0 = right, 1 = left, 2 = up, 3 = down
        if self.direction == 0:
            if self.target_x > self.rect.x and self.allowed_direction[0]:
                self.rect.x += self.speed
            elif not self.allowed_direction[0]:
                if self.target_y > self.rect.y and self.allowed_direction[3]:
                    self.direction = 3
                    self.rect.y += self.speed
                elif self.target_y < self.rect.y and self.allowed_direction[2]:
                    self.direction = 2
                    self.rect.y -= self.speed
                elif self.target_x < self.rect.x and self.allowed_direction[1]:
                    self.direction = 1
                    self.rect.x -= self.speed
                elif self.allowed_direction[3]:
                    self.direction = 3
                    self.rect.y += self.speed
                elif self.allowed_direction[2]:
                    self.direction = 2
                    self.rect.y -= self.speed
                elif self.allowed_direction[1]:
                    self.direction = 1
                    self.rect.x -= self.speed
            elif self.allowed_direction[0]:
                self.rect.x += self.speed

        elif self.direction == 1:
            if self.in_box and self.target_y < self.rect.y and self.allowed_direction[2]:
                self.direction = 2
                self.rect.y -= self.speed
            elif self.target_y > self.rect.y and self.allowed_direction[3]:
                self.direction = 3
            elif self.target_x < self.rect.x and self.allowed_direction[1]:
                self.rect.x -= self.speed
            elif not self.allowed_direction[1]:
                if self.target_y > self.rect.y and self.allowed_direction[3]:
                    self.direction = 3
                    self.rect.y += self.speed
                elif self.target_y < self.rect.y and self.allowed_direction[2]:
                    self.direction = 2
                    self.rect.y -= self.speed
                elif self.target_x > self.rect.x and self.allowed_direction[0]:
                    self.direction = 0
                    self.rect.x += self.speed
                elif self.allowed_direction[3]:
                    self.direction = 3
                    self.rect.y += self.speed
                elif self.allowed_direction[2]:
                    self.direction = 2
                    self.rect.y -= self.speed
                elif self.allowed_direction[0]:
                    self.direction = 0
                    self.rect.x += self.speed
            elif self.allowed_direction[1]:
                self.rect.x -= self.speed

        elif self.direction == 2:
            if self.target_x < self.rect.x and self.allowed_direction[1]:
                self.direction = 1
                self.rect.x -= self.speed 
            elif self.target_y < self.rect.y and self.allowed_direction[2]:
                self.direction = 2
                self.rect.y -= self.speed
            elif not self.allowed_direction[2]:
                if self.target_x > self.rect.x and self.allowed_direction[0]:
                    self.direction = 0
                    self.rect.x += self.speed
                elif self.target_x < self.rect.x and self.allowed_direction[1]:
                    self.direction = 1
                    self.rect.x -= self.speed
                elif self.target_y > self.rect.y and self.allowed_direction[3]:
                    self.direction = 3
                    self.rect.y += self.speed
                elif self.allowed_direction[1]:
                    self.direction = 1
                    self.rect.x -= self.speed
                elif self.allowed_direction[3]:
                    self.direction = 3
                    self.rect.y += self.speed
                elif self.allowed_direction[0]:
                    self.direction = 0
                    self.rect.x += self.speed
            elif self.allowed_direction[2]:
                if self.target_x > self.rect.x and self.allowed_direction[0]:
                    self.direction = 0
                    self.rect.x += self.speed
                elif self.target_x < self.rect.x and self.allowed_direction[1]:
                    self.direction = 1
                    self.rect.x -= self.speed
                else:
                    self.rect.y -= self.speed

        elif self.direction == 3:
            if self.target_y > self.rect.y and self.allowed_direction[3]:
                self.rect.y += self.speed 
            elif not self.allowed_direction[3]:
                if self.target_x > self.rect.x and self.allowed_direction[0]:
                    self.direction = 0
                    self.rect.x += self.speed 
                elif self.target_x < self.rect.x and self.allowed_direction[1]:
                    self.direction = 1
                    self.rect.x -= self.speed
                elif self.target_y < self.rect.y and self.allowed_direction[2]:
                    self.direction = 2
                    self.rect.y -= self.speed
                elif self.allowed_direction[2]:
                    self.direction = 2
                    self.rect.y -= self.speed
                elif self.allowed_direction[1]:
                    self.direction = 1 
                    self.rect.x -= self.speed
                elif self.allowed_direction[0]:
                    self.direction = 0
                    self.rect.x += self.speed
            elif self.allowed_direction[3]:
                if self.target_x > self.rect.x and self.allowed_direction[0]:
                    self.direction = 0
                    self.rect.x += self.speed
                elif self.target_x < self.rect.x and self.allowed_direction[1]:
                    self.direction = 1
                    self.rect.x -= self.speed
                else:
                    self.rect.y += self.speed

    def update(self):
        self.clamp()
        self.get_target()
        if not self.player.is_dying:
            if self.eaten:
                self.move_clyde()
            else:
                if self.name == 'blinky':
                    self.move_blinky()
                elif self.name == 'inky':
                    self.move_inky()
                elif self.name == 'pinky':
                    self.move_pinky()
                elif self.name == 'clyde':
                    self.move_clyde()
        self.draw()

    def draw(self):
        self.image = self.timer.current_image()
        self.screen.blit(self.image, self.rect)
    

class Ghosts():
    def __init__(self, game):
        self.game = game
        self.player = game.player
        self.stats = game.stats
        self.sound = game.sound
        self.sb = game.sb

        self.ghost_group = pg.sprite.Group()

    def make_ghost(self, x, y, ghost_num):
        ghost = Ghost(game=self.game, ghost_num = ghost_num)
        ghost.rect.x = x
        ghost.rect.y = y
        self.ghost_group.add(ghost)

    def make_ghosts(self):
        x, y = 330, 260         # in box: x=300, y=324
        num_ghosts = 0

        while num_ghosts < 4:
            self.make_ghost(x=x, y=y, ghost_num = num_ghosts)
            x = 300
            y = 324
            x += num_ghosts * 30
            num_ghosts += 1
            

    def reset(self):
        self.ghost_group.empty()

    def update(self):
        hit_ghost = pg.sprite.spritecollideany(self.player, self.ghost_group)      # returns None or ghost that's collided

        if hit_ghost is not None:
            if self.player.power_up and not hit_ghost.eaten and not hit_ghost.is_dying:
                hit_ghost.is_dying = True
                hit_ghost.eaten = True
                self.sound.play_eat()
                self.stats.score += 400
                self.sb.check_high_score()
            elif not self.player.power_up and hit_ghost.timer == hit_ghost.regtimer:
                self.sound.run_ghost.stop()
                self.sound.move_ghost.stop()
                self.ghost_group.empty()
                self.player.hit()

        if not self.ghost_group:
            self.make_ghosts()

        for ghost in self.ghost_group.sprites():
            if (not self.player.power_up and not ghost.is_dying) or (ghost.eaten and self.player.power_up and not ghost.is_dying):
                ghost.timer = ghost.regtimer
                ghost.speed = 2
                if self.sound.run_ghost.get_num_channels() > 0:
                    self.sound.run_ghost.stop()
                if not self.game.just_restarted and not self.player.is_dying and self.sound.move_ghost.get_num_channels() == 0:
                    self.sound.play_move()
            elif ghost.eaten:
                ghost.timer = ghost.eyestimer
                ghost.speed = 7
            elif self.player.power_up:
                ghost.timer = ghost.runtimer
                if self.sound.move_ghost.get_num_channels() > 0:
                    self.sound.move_ghost.stop()
                if self.sound.run_ghost.get_num_channels() == 0:
                    self.sound.play_run()
                ghost.speed = 2

            if not self.player.power_up and not ghost.timer == ghost.eyestimer:
                ghost.eaten = False

            ghost.update()
