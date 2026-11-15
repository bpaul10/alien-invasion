""""
Program name: Ultra Alien Invasion
Author: Bernard Paul
Purpose: vault class that is managing the player's available boosters (possibly) and bullet types along with firing modes
Date: 11/14/2026
"""
import pygame
from bullet import Bullet


class Vault:
    """Manager for the players bullets and firing types along with available boosters"""
    def __init__(self, ai_game):
        "initialize the vault which is the weapons system"
        self.ai_game = ai_game
        self.ship = ai_game.ship
        self.settings = ai_game.settings
        self.bullets = pygame.sprite.Group()

        self.time_last_shot = 0 #varibale to know when the last shot was fired 

    def fire(self):
        """firing bullets by using the current firing mode"""
        current_time = pygame.time.get_ticks() #using the pygame library this will get the current time in milliseconds 


        if(current_time - self.time_last_shot<self.settings.normal_shooting_speed):
            return

        if self.ship.triple_shot_active:
            angles = [-15, 0, 15]

        else:
            angles = [0]

        
        if len(self.bullets) + len(angles) > self.settings.bullets_allowed:
            return

        self.time_last_shot = current_time

        if self.ship.triple_shot_active:
            #this will make it shoot in 3 different angles 
            angles = [-15, 0, 15] 
            for angle in angles:
                new_bullet = Bullet(self.ai_game,  angle)
                self.bullets.add(new_bullet)

        else:
            #will just fire normal bullets
            new_bullet = Bullet(self.ai_game, 0)
            self.bullets.add(new_bullet)


    def update(self):
        """this will update the bullet positions and remove the bullets once they reach outside the screen"""
        self.bullets.update()

        #remove bullets that have left the screen
        for bullet in self.bullets.copy():
            if(bullet.rect.bottom<0 or bullet.rect.right<0 or bullet.rect.left>self.settings.screen_width):
                self.bullets.remove(bullet)


    def draw(self):
        """this will draw the bullets on the screen"""
        for bullet in self.bullets.sprites():
            bullet.draw()
