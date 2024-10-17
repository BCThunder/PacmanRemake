import pygame as pg
from pygame.sprite import Sprite
from timer import Timer
import time

class Player(Sprite):
    img_names = ["pacman1.png", "pacman2.png", "pacman3.png"]
    img_files = [pg.image.load(f"pacman_imgs/{name}") for name in img_names]
    imgs = [pg.transform.scale(x, (32, 32)) for x in img_files]

    death_names = ["death1.png", "death2.png", "death3.png", "death4.png", "death5.png", "death6.png"]
    death_files = [pg.image.load(f"pacman_imgs/{name}") for name in death_names]
    death_anim = [pg.transform.scale(x, (32, 32)) for x in death_files]

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.screen_height = self.settings.screen_height
        self.screen_width = self.settings.screen_width
        self.map = game.map.map
        self.stats = game.stats
        self.points = game.settings.pellet_points
        self.sound = game.sound

        self.regtimer = Timer(Player.imgs, start_index = 0, delta = 6)
        self.deathtimer = Timer(Player.death_anim, start_index = 0, delta = 8, looponce = True)
        self.timer = self.regtimer
        self.image = Player.imgs[0]

        self.rect = self.image.get_rect()
        self.rect.x = self.settings.start_x
        self.rect.y = self.settings.start_y

        self.direction = 0
        self.lives = self.settings.player_lives
        self.allowed_direction = [False, False, False, False]
        self.center_x = self.rect.centerx      # 360
        self.center_y = self.rect.centery      # 539
        self.speed = self.settings.player_speed
        self.in_tunnel = False
        self.power_up = False
        self.power_up_timer = 0
        self.ghost_eaten = [False, False, False, False]
        self.is_dying = False

    def set_sb(self, sb): self.sb = sb

    def set_direction(self, input):
        self.direction = input
        if not self.is_dying and self.sound.waka_waka.get_num_channels() == 0:
            self.sound.play_waka()
        self.update()

    def clamp(self):
        self.center_x = self.rect.centerx
        self.center_y = self.rect.centery
        num1 = ((self.screen_height - 40) // 32)  # num1 = 22   screen_height = 760
        num2 = (self.screen_width // 30)        # num2 = 24     screen_width = 720
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
            if self.center_x // 30 < 29:
                if self.direction == 0:
                    if self.map[self.center_y // num1][(self.center_x - buffer) // num2] < 3:
                        self.allowed_direction[1] = True
                if self.direction == 1:
                    if self.map[self.center_y // num1][(self.center_x + buffer) // num2] < 3:
                        self.allowed_direction[0] = True
                if self.direction == 2:
                    if self.map[(self.center_y + buffer) // num1][self.center_x // num2] < 3:
                        self.allowed_direction[3] = True
                if self.direction == 3:
                    if self.map[(self.center_y - buffer) // num1][self.center_x // num2] < 3:
                        self.allowed_direction[2] = True

                if self.direction == 2 or self.direction == 3:
                    if 9 <= self.center_x % num2 <= 15:
                        if self.map[(self.center_y + buffer) // num1][self.center_x // num2] < 3:
                            self.allowed_direction[3] = True
                        if self.map[(self.center_y - buffer) // num1][self.center_x // num2] < 3:
                            self.allowed_direction[2] = True
                    if 8 <= self.center_y % num1 <= 14:
                        if self.map[self.center_y // num1][(self.center_x - num2) // num2] < 3:
                            self.allowed_direction[1] = True
                        if self.map[self.center_y // num1][(self.center_x + num2) // num2] < 3:
                            self.allowed_direction[0] = True

                if self.direction == 0 or self.direction == 1:
                    if 9 <= self.center_x % num2 <= 15:
                        if self.map[(self.center_y + num1) // num1][self.center_x // num2] < 3:
                            self.allowed_direction[3] = True
                        if self.map[(self.center_y - num1) // num1][self.center_x // num2] < 3:
                            self.allowed_direction[2] = True
                    if 8 <= self.center_y % num1 <= 14:
                        if self.map[self.center_y // num1][(self.center_x - buffer) // num2] < 3:
                            self.allowed_direction[1] = True
                        if self.map[self.center_y // num1][(self.center_x + buffer) // num2] < 3:
                            self.allowed_direction[0] = True


            else:
                self.allowed_direction[0] = True
                self.allowed_direction[1] = True

    def check_collisions(self):
        num1 = (self.screen_height - 50) // 32  # map row index
        num2 = (self.screen_width) // 30        # map col index
        if self.in_tunnel is False:
            if self.map[self.center_y // num1][self.center_x // num2] == 1:
                self.stats.score += self.points
                self.map[self.center_y // num1][self.center_x // num2] = 0
                self.sb.check_high_score()
            if self.map [self.center_y // num1][self.center_x // num2] == 2:
                self.stats.score += 5 * self.points
                self.map[self.center_y // num1][self.center_x // num2] = 0
                self.power_up = True
                self.power_up_timer = 0
                self.sound.play_power_up() 
                self.sb.check_high_score()     

    def get_allowed_directions(self): return self.allowed_direction
    
    def move(self):
        # r, l, u, d
        if self.direction == 0 and self.allowed_direction[self.direction]:
            self.rect.x += self.speed
        elif self.direction == 1 and self.allowed_direction[self.direction]:
            self.rect.x -= self.speed
        elif self.direction == 2 and self.allowed_direction[self.direction]:
            self.rect.y -= self.speed
        elif self.direction == 3 and self.allowed_direction[self.direction]:
            self.rect.y += self.speed
            
    def set_imgs(self):
        self.image = Player.imgs[2]

    def hit(self):
        time.sleep(0.3)
        self.timer = self.deathtimer
        self.is_dying = True
        self.sound.waka_waka.stop()
        self.sound.play_death()
        self.stats.lives_left -= 1
        self.sb.prep_lives()
        if self.stats.lives_left <= 0:
            self.deathtimer.index = 0
            self.timer = self.regtimer
            self.is_dying = False
            time.sleep(1)
            self.game.game_over()
        else:
            self.game.reset()

    def reset(self):
        self.rect.x = self.settings.start_x
        self.rect.y = self.settings.start_y
        self.power_up = False

    def update(self):
        self.clamp()
        if not self.is_dying:
            self.move()
        self.check_collisions()
        self.draw()
        self.sb.prep()

        if self.power_up and self.power_up_timer < 550:
            self.power_up_timer += 1
        else:
            self.power_up = False
            self.power_up_timer = 0

    def draw(self):
        self.image = self.timer.current_image()

        # 0-Right, 1-Left, 2-Up, 3-Down
        if self.timer == self.regtimer and not self.is_dying:
            if self.direction == 0 and self.allowed_direction[self.direction]:
                self.screen.blit(self.image, self.rect)
            elif self.direction == 1 and self.allowed_direction[self.direction]:
                self.screen.blit(pg.transform.flip(self.image, True, False), self.rect)
            elif self.direction == 2 and self.allowed_direction[self.direction]:
                self.screen.blit(pg.transform.rotate(self.image, 90), self.rect)
            elif self.direction == 3 and self.allowed_direction[self.direction]:
                self.screen.blit(pg.transform.rotate(self.image, 270), self.rect)
            else: 
                self.screen.blit(self.image, self.rect)
        elif self.timer == self.deathtimer:
            self.screen.blit(self.image, self. rect)

        if self.is_dying and self.timer.finished():
            self.deathtimer.index = 0
            self.timer = self.regtimer
            self.is_dying = False
            time.sleep(1)