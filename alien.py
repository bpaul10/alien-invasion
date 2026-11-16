"""
program name: ultra alien invasion
Author: Bernard Paul 
Purpose:this file manages the alien sprite
starter link:
date updated: 11/15/26

"""

import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """nitialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        # start each new alien near the top left of the screen. 
        self.rect.x = self.rect.width
        self.rect.y - self.rect.height

        #store the aliens exact horizontal position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def check_edges(self):
        """return True if alien is at edge of screen"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)


    def update(self):
        """move the alien to the right and down"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
        self.y += self.settings.alien_speed
        self.rect.y = self.y

        if self.rect.left > self.screen.get_rect().right:
            self.rect.right = 0
            self.x = float(self.rect.x)

    def reset_position(self):
        """will reset the alien's position to the top after its collided"""

        self.rect.midtop = self.screen.get_rect().midtop
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)