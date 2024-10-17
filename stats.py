class Stats:
    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        self.reset()
        self.score = 0
        hs_file = open("highscore.json", "r")
        self.high_score = int(hs_file.read())
        hs_file.close()

    def set_player(self, player):
        self.player = player

    def reset(self):
        self.lives_left = self.settings.player_lives
        self.score = 0