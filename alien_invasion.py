"""
program name: ultra alien invasion
Author: Bernard Paul 
Purpose: this is the main alien invasion file that runs the main game 
starter link:
date updated: 11/15/26

"""
import sys
from time import sleep
import pygame 
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button

from ship import Ship
from bullet import Bullet
from alien import Alien
from vault import Vault



class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game, cand create game resources"""
        pygame.init()

        self.clock = pygame.time.Clock() #creates the game clock which controls frame rate
        self.settings = Settings() #loads the game settings
        self.font = pygame.font.SysFont(None, 36) #making the font for the displaying health and ability info 
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) #creates the game window in full screen
        #screen dimensions of the game based off the actual screen
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        #displays the game name 
        pygame.display.set_caption("Ultra Alien Invasion -Track 1 Mechnics")

        # Create an instance to store game statistics.
        self.stats = GameStats(self)
        #self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.vault = Vault(self) #vault manages the players bullets 

        
        self.bullets = pygame.sprite.Group() #makes the group that stores the bullets
        self.aliens = pygame.sprite.Group() #makes the group the stores the aliens
        #self._create_fleet()
        self._create_alien() #will create an alien

        #start Alien Invasion in an active state
        self.game_active = True
        #self.play_button = Button(self, "Play")  
        self.game_over = False
        

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            if self.game_active and not self.game_over:
                self.ship.update()
                self._update_aliens()
                self._update_bullets()
                self.vault.update()
                self._check_bullet_alien_collisions()
            self._update_screen()
            self.clock.tick(60)



    def _check_events(self):
        """respond to keypresses and mouse events"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            """            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            """
    def _check_play_button(self, mouse_pos):
        """start a new game when the player clicks Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        
        if button_clicked and not self.game_active:
            #rest the game settings 
            self.settings.initialize_dynamic_settings()
            #will reset the game statistics
            self.stats.reset_stats()
            #self.sb.prep_score()
            #self.sb.prep_level()
            #self.sb.prep_ships()



            self.game_active = True
            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            #create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)
            


    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            if not self.game_over:
                self.vault.fire()

        elif event.key == pygame.K_s:
            if not self.game_over:
                self.ship.activate_shield()

        elif event.key == pygame.K_t:
            if not self.game_over:
                self.ship.activate_triple_shot()

        elif event.key == pygame.K_r:
            if self.game_over:
                self._restart_game()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:

            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                 self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()
    def _check_bullet_collisions(self):
        """Remove aliens when bullets hit them."""
        pygame.sprite.groupcollide(
            self.arsenal.bullets,
            self.aliens,
            True,
            True
        )

        if not self.aliens:
            self._create_alien()
    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
                self.vault.bullets,
                self.aliens,
                True,
                True
            )

        if collisions:
            print("ALIEN DESTROYED!")

            # Create another alien when all aliens are destroyed.
        if not self.aliens:
            self._create_alien()
            
    def _create_fleet(self):
        """create the fleet of aliens"""
        #create an alien and keep doing until there is no room
        #spacing between aliens is one alient width and one alien hieght 

        # make an alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):

            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

                #finished a rowl reset x value, and incremented y value 
            current_x = alien_width
            current_y += 2 * alien_height
    def _create_alien(self): #might have to add back in x_position, y_position
        """Create an alien and place it in the fleet"""
        new_alien = Alien(self)
        """     
        probably wont need this part of code anymore but keeping in case 
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        
        """
        self.aliens.add(new_alien)



    def _update_aliens(self):
        """check if the fleet is at an edge then update positions"""
        if self.game_over or not self.game_active:
            return

        self._check_fleet_edges()
        self.aliens.update()

        for alien in self.aliens.sprites():
            if alien.rect.colliderect(self.ship.rect):

                if self.ship.shield_active:
                    alien.reset_position()

                elif self.ship.take_damage():
                    alien.reset_position()

                    if self.ship.health <= 0:
                        self.game_over = True

            elif alien.rect.top >= self.settings.screen_height:
                alien.reset_position()
            


    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        """drop the entire fleet and change the fleets direction"""

        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0:

            #decrement ships_left, and update scoreboard
            self.stats.ships_left -=1
            #self.sb.prep_ships()
            #get rid of any remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            #create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            #creates a pause
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
            
    def _check_aliens_bottom(self):
        """check if any aliens have reached the bottom of the screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                #treat thois same as if the ship got hit
                self._ship_hit()
                break 

    def _restart_game(self):
        """will reset the player and enemy for another game """
        self.ship.health = self.settings.ship_health
        self.ship.center_ship()

        self.ship.shield_active = False
        self.ship.triple_shot_active = False
        self.ship.shield_end_time = 0
        self.ship.triple_shot_end_time = 0
        self.vault.bullets.empty()
        self.aliens.empty()
        self._create_alien()
        self.game_over = False
        self.game_active = True #might not need this part


    def _draw_health_bar(self):
        """drawing the players health bar"""
        bar_x =20
        bar_y = 20
        bar_width = 200
        bar_height = 25
        pygame.draw.rect(self.screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))

        health_width = int(bar_width * (self.ship.health / self.settings.ship_health))

        if self.ship.health > 50:
            health_color = (0, 200, 0)
        elif self.ship.health > 25:
            health_color = (255, 165, 0)
        else:
            health_color = (255, 0, 0)

        pygame.draw.rect(self.screen, health_color, (bar_x, bar_y, health_width, bar_height))


        health_text = self.font.render(f"Health: {self.ship.health}", True, (255, 255, 255))
        self.screen.blit(health_text, (20,55))

    def _draw_ability_status(self):
        """display if the shield and triple shot ability are active"""
        shield_status = ("ACTIVE" if self.ship.shield_active else "INACTIVE")

        triple_shot_status = ("ACTIVE" if self.ship.triple_shot_active else "INACTIVE")
        shield_text = self.font.render(f"Shield (S): {shield_status}", True, self.settings.shield_color)
        triple_shot_text = self.font.render(f"Triple Shot (T): {triple_shot_status}", True, (150, 0,150))

        self.screen.blit(shield_text, (20, 90))
        self.screen.blit(triple_shot_text, (20, 120))


    def _update_screen(self):
        """update image on the screen, and flip to the new screen."""

            #redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.vault.draw()
        self._draw_health_bar()
        self._draw_ability_status()

        # draw the score information
        #self.sb.show_score()

        if self.game_over:
            game_over_text = pygame.font.SysFont(None, 70).render("Game over - r to restart", True, (200, 0, 0))
            text_rect = game_over_text.get_rect(center=self.screen.get_rect().center)
            self.screen.blit(game_over_text, text_rect)
        # draw the play buitton if the game is inactive
        """        
        if not self.game_active:
            self.play_button.draw_button()
        


            #Make the most recently drawn screeen visible"""
        
        pygame.display.flip()

    
if __name__ == '__main__':
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()