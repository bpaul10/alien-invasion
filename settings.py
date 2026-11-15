

class Settings:
    """ A class to store all the settings for alien invasion"""

    def __init__(self):
        """ intializie the game's static settings"""
        #screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        #ships settings
        self.ship_speed = 1.5
        self.ship_limit = 3
        self.ship_health = 100 #adding ship health to the game


        # Bullet settings
        self.bullet_speed = 2.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 9 
        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right -1 represents left
        self.fleet_direction = 1

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        # how quicklyt he alien point value increases
        self.score_scale = 1.5

        # Having different shooting types normal and rapid
        self.normal_shooting_speed = 350 
        self.rapid_shooting_speed = 5.0

        # Going to make a triple shot
        self.triple_shot_time = 3 #will have triple shot for 3 seconds
        self.triple_shot_cooldown = 4 #will have a 4 second cooldown

        # settings for rapid firing 
        self.rapid_firing_time = 3 #will have rapid firing for 3 seconds
        self.rapid_firing_cooldown = 4 #will have a 4 second cooldown

        #settings for the shield
        self.shield_time = 3 #will have the shield for 3 seconds
        self.shield_cooldown = 4 #will have a 4 second cooldown

        #shield ability color 
        self.shield_color = (0, 0, 255)

        #damage settings
        self.damage_amount=25
        self.damage_cooldown =1000


        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
        #scoring settings
        self.alien_points = 50


    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)