import pygame as pg
import pygame.font 
from pygame.sprite import Group
from player import Player


class Scoreboard:
	def __init__(self, game):
		self.game = game 
		self.screen = game.screen 
		self.screen_rect = game.screen.get_rect() 
		self.settings = game.settings 
		self.stats = game.stats
		self.player = game.player
		self.screen_height = self.settings.screen_height
		self.screen_width = self.settings.screen_width

		self.text_color = 'white'
		self.font = pg.font.SysFont(None, 30)
		self.prep()
		self.prep_high_score()

	def prep(self):
		self.prep_score()
		self.prep_lives()

	def prep_score(self):
		rounded_score = round(self.stats.score, -1)
		s = f'Score: {rounded_score:,}'

		self.score_image = self.font.render(s, True, self.text_color)
		self.score_rect = self.score_image.get_rect()
		self.score_rect.x = 20
		self.score_rect.y = self.screen_height - 50

	def prep_high_score(self):
		self.high_score = round(self.stats.high_score, -1)
		self.high_score_str = f"High: {self.high_score:,}"

		self.high_score_image = self.font.render(self.high_score_str, True, self.text_color)
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = self.score_rect.top

	def prep_lives(self):
		self.players = Group()
		for player_number in range(self.stats.lives_left):
			player = Player(self.game)
			player.set_imgs()
			player.rect.x = 615 + player_number * player.rect.width
			player.rect.y = self.screen_height - 38
			self.players.add(player)

	def check_high_score(self):
		if self.stats.score > self.stats.high_score:
			self.stats.high_score = self.stats.score
			self.prep_high_score()

	def update(self): 
		self.draw()

	def draw(self):
		self.screen.blit(self.score_image, (10, self.screen_height-30))
		self.screen.blit(self.high_score_image, (200, self.screen_height-30))
		self.players.draw(self.screen)
