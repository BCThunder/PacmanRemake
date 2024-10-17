import pygame as pg
from pygame import mixer 
import time


class Sound:
    def __init__(self):
        mixer.init()
        self.start_sound = mixer.Sound("pacman_sounds/start.wav")       # 4.35 seconds
        self.death_sound = mixer.Sound("pacman_sounds/death.wav")       # 1.62 seconds
        self.eat_ghost = mixer.Sound("pacman_sounds/eat_ghost.wav")
        self.run_ghost = mixer.Sound("pacman_sounds/run.wav")
        self.waka_waka = mixer.Sound("pacman_sounds/waka_waka.wav")
        self.move_ghost = mixer.Sound("pacman_sounds/ghost_moving.wav")
        self.power_up = mixer.Sound("pacman_sounds/power_up.wav") 
        self.volume = 0.1
        self.set_volume(self.volume)        
    
    def set_volume(self, volume=0.3):
        self.start_sound.set_volume(3 * volume)
        self.death_sound.set_volume(2 * volume)
        self.eat_ghost.set_volume(2 * volume)
        self.run_ghost.set_volume(2 * volume)
        self.waka_waka.set_volume(volume)
        self.move_ghost.set_volume(3 * volume)
        self.power_up.set_volume(2.5 * volume) 
 
    def play_start(self): 
        mixer.Sound.play(self.start_sound) 

    def play_death(self):
        mixer.Sound.play(self.death_sound)

    def play_eat(self):
        mixer.Sound.play(self.eat_ghost)

    def play_run(self):
        mixer.Sound.play(self.run_ghost)

    def play_waka(self):
        mixer.Sound.play(self.waka_waka)

    def play_power_up(self):
        mixer.Sound.play(self.power_up)

    def play_move(self):
        mixer.Sound.play(self.move_ghost)

    def play_game_over(self):
        mixer.pause()
        self.stop_music()
        mixer.Sound.play(self.game_over)
        time.sleep(2.5)