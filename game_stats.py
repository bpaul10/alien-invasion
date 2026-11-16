"""
program name: ultra alien invasion
Author: Bernard Paul 
Purpose: does not apply for milestone 1 but create the game stats of the game such as the score and level 
starter link:
date updated: 11/15/26

"""



class GameStats:
    """track stats for alien invasion"""

    def __init__(self, ai_game):
        """initialize statistics"""
        self.settings = ai_game.settings
        self.reset_stats()
        #high score should never be reset
        self.high_score = 0



    def reset_stats(self):
        """initlaize statistics that can change during game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1