"""
Program name: Ultra Alien Invasion
Author: Bernard Paul
Purpose: bullet class that is managing the players projectiles 
Date: 11/14/2026


"""


import math #going to be using math import for calculations and angles 
import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """ class to manage bullets fired from the ship."""


    def __init__(self, ai_game, angle=0): 
        """create a bullet object at the ship's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
            self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store the bullet's position as a float.
        self.y = float(self.rect.y)
        self.x = float(self.rect.x) #have to make a x value 

        #gpoing to have an angel for the projectiles now which will be in radians
        radians = math.radians(angle) #using the math import we can do angles in radians 

        #we will now be having velocity components based on the angle (might switch to degrees instead of rad)
        self.velocity_x = self.settings.bullet_speed * math.sin(radians)
        self.velocity_y = -self.settings.bullet_speed * math.cos(radians)


    def update(self):
        """Move the bullet up the screen"""

        #update the exact position of the bullet now having it in x and y values 
        self.x += self.velocity_x
        self.y += self.velocity_y
        #update the rect position with x and y values 
        self.rect.x = self.x
        self.rect.y = self.y


    def draw_bullet(self):
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)

        