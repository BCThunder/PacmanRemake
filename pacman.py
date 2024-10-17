import pygame as pg
import sys, time
from settings import Settings
from map import Map
from player import Player
from ghost import Ghosts
from scoreboard import Scoreboard
from stats import Stats
from button import Button
from sound import Sound

class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.screen = pg.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.input = 0

        self.sound = Sound()
        self.stats = Stats(game=self)
        self.map = Map(game=self)
        self.player = Player(game=self)
        self.sb = Scoreboard(game=self)
        self.ghosts = Ghosts(game=self)
        self.player.set_sb(self.sb)
        self.game_active = True
        self.won = False
        self.just_restarted = True
        self.level = 0
        self.retry_button = Button(game=self, text="Retry?")

    def check_events(self):
        for event in pg.event.get():
            type = event.type
            if type == pg.KEYUP: 
                key = event.key
            elif type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif type == pg.MOUSEBUTTONDOWN:
                b = self.retry_button
                x, y = pg.mouse.get_pos()
                if b.rect.collidepoint(x, y):
                    b.press()
            elif type == pg.MOUSEMOTION:
                b = self.retry_button
                x, y = pg.mouse.get_pos()
                b.select(b.rect.collidepoint(x, y))
            elif type == pg.KEYDOWN:
                key = event.key
                if key == pg.K_RIGHT:
                    self.input = 0
                elif key == pg.K_LEFT:
                    self.input = 1
                elif key == pg.K_UP:
                    self.input = 2
                elif key == pg.K_DOWN:
                    self.input = 3
            elif type == pg.KEYUP:
                key = event.key
                if key == pg.K_RIGHT and self.input == 0:
                    self.input = self.player.direction
                elif key == pg.K_LEFT and self.input == 1:
                    self.input = self.player.direction
                elif key == pg.K_UP and self.input == 2:
                    self.input = self.player.direction
                elif key == pg.K_DOWN and self.input == 3:
                    self.input = self.player.direction

        if self.game_active:
            if self.input == 0 and self.player.get_allowed_directions()[0]:
                self.player.set_direction(0)
            if self.input == 1 and self.player.get_allowed_directions()[1]:
                self.player.set_direction(1)
            if self.input == 2 and self.player.get_allowed_directions()[2]:
                self.player.set_direction(2)
            if self.input == 3 and self.player.get_allowed_directions()[3]:
                self.player.set_direction(3)

    def game_over(self):
        pg.mouse.set_visible(True)
        self.retry_button.show()
        self.game_active = False
        self.map.wall_color = self.map.wall_colors[0]

        hs_file = open("highscore.json", 'w')
        hs_file.write(str(self.sb.high_score))
        hs_file.close()

        self.stats.reset()

    def activate(self):
        self.game_active = True
            
    def reset(self):
        self.ghosts.reset()
        self.player.reset()

    def check_win(self):
        self.won = True
        if self.map.check_win() is False:
            self.won = False

    def restart_game(self):
        self.reset()
        self.reset_map()
        self.activate()

    def reset_map(self):
        self.map.reset()
        self.player.map = self.map.map

    def play(self):
        active = True
        self.screen.fill('black')

        while active:
            self.check_events()

            if self.game_active:
                self.screen.fill('black')
                self.map.draw_map()
                self.player.update()
                self.sb.update()
                self.ghosts.update()
                self.check_win()

                if self.won:
                    self.level += 1
                    self.map.wall_color = self.map.wall_colors[self.level % 3]
                    self.reset_map()
                    self.reset()

            else:
                self.retry_button.update()

            pg.display.flip()
            time.sleep(0.02)

            if self.just_restarted:
                    self.just_restarted = False
                    self.sound.play_start()
                    time.sleep(4.35)

if __name__ == '__main__':
  g = Game()
  g.play()
