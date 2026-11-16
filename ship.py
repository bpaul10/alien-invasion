"""
program name: ultra alien invasion
Author: Bernard Paul 
Purpose: this will manage the ship movement health shield and triple shot
starter link:
date updated: 11/15/26

"""

from pathlib import Path
import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """A class to manage the ship"""

    def __init__(self, ai_game):
        """Initialize the ship and set its stareting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #load the ship image and get its rect.

        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        #start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        #store a flaot for the ships exact horizontal position
        self.x = float(self.rect.x)

        #movement flag; start with a ship thats not moving 

        self.moving_right = False
        self.moving_left = False


        self.health = self.settings.ship_health

        #shield ability stuff
        self.shield_active = False
        self.shield_end_time = 0
        self.shield_ready_time = 0

        #the triple shot values
        self.triple_shot_active = False
        self.triple_shot_end_time = 0
        self.triple_shot_ready_time = 0

        #for the cooldown of damage
        self.last_damage_time = 0

    def update(self):
        """Updates teh ship position based on the movement flag"""
        # Update the ship's x value, not the rect.

        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x

        #adding this for the abilities
        self.update_abilities()

    def update_abilities(self):
        """this will deactivate the abilities when their timers expire """

        current_time = pygame.time.get_ticks()

        if current_time >= self.shield_end_time:
            self.shield_active = False

        if current_time >= self.triple_shot_end_time:
            self.triple_shot_active = False

    def activate_shield(self):
        """this will actviate teh shield if the cool down is ready adn the player chooses to """
        current_time = pygame.time.get_ticks()

        if current_time >= self.shield_ready_time:
            self.shield_active = True
            self.shield_end_time = current_time + self.settings.shield_time
            self.shield_ready_time = current_time + self.settings.shield_time + self.settings.shield_cooldown


    def activate_triple_shot(self):
        """activate the triple shot if the cooldown is ready and the player chooses to"""
        current_time = pygame.time.get_ticks()

        if current_time >= self.triple_shot_ready_time:
            self.triple_shot_active = True
            self.triple_shot_end_time = current_time + self.settings.triple_shot_time
            self.triple_shot_ready_time = current_time + self.settings.triple_shot_time + self.settings.triple_shot_cooldown


    def take_damage(self):
        """will reduce the ships health when damage happens"""
        current_time = pygame.time.get_ticks()

        if self.shield_active:
            return False

        if current_time - self.last_damage_time < self.settings.damage_cooldown:
            return False

        self.health -= self.settings.damage_amount
        self.health = max(0, self.health)
        self.last_damage_time = current_time
        return True

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

        # update rect object from self.x
        self.rect.x = self.x
    def blitme(self):
        """Draw the ship at its current location and now its shield too"""
        self.screen.blit(self.image, self.rect)
        if self.shield_active:
            pygame.draw.circle(self.screen, self.settings.shield_color, self.rect.center, max(self.rect.width, self.rect.height) // 2+10, 4)