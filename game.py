# https://www.youtube.com/watch?v=RHMrds9l6nY

import pygame, sys
from pygame.locals import *
import time
import random

width_or_height = 500
screen_width = width_or_height
screen_height = width_or_height
pygame.font.init()

window = pygame.display.set_mode((screen_width, screen_height))
window.fill('light blue')

tanks = []
rockets = []
speed = 1000
num_sprites = 2


class Game:

    def __init__(self):
        self.energy_released = 0
        # self.explosion_sound = pygame.mixer.music.load("explosion.wav")
        pygame.mixer.init()

    # Creates all sprites
    def create_sprites(self):
        for i in range(num_sprites):
            tank = Tank(random.randint(10, screen_width),
                        random.randint(10, screen_height), 64, i)
            tank.load()
            tanks.append(tank)
            rocket = Rocket(random.randint(10, screen_width),
                            random.randint(10, screen_height), 64, i)
            rocket.load()
            rockets.append(rocket)

    # Each iteration is a frame
    def render_frames(self):
        while True:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                break

            # Set up all positions
            for tank in tanks:
                tank.move()
                time.sleep(1/speed)

            for rocket in rockets:
                rocket.move()
                time.sleep(1/speed)

            # Cleans the screen
            window.fill('light blue')

            # Draws all objects
            for tank in tanks:
                tank.draw()
                # print(tank.sprite_x, tank.sprite_y)
            for rocket in rockets:
                rocket.draw()

            # Checks for collisions
            all_sprites = tanks + rockets
            for sprite in all_sprites:
                for other_sprite in all_sprites:
                    if sprite.name != other_sprite.name:
                        if sprite.check_and_change_direction(other_sprite) == True:
                            if sprite.type == other_sprite.type:
                                sprite.energy += 1
                                other_sprite.energy += 1
                                print('Sprite Energy', sprite.energy, 'Other Sprite Energy', other_sprite.energy)
                            elif sprite.type != other_sprite.type:
                                if sprite.killed == False and other_sprite.killed == False:
                                    self.energy_released += (sprite.energy + other_sprite.energy)
                                    sprite.kill_sprite()
                                    other_sprite.kill_sprite()


                                    # pygame.mixer.music.load("explosion.wav")
                                    # pygame.mixer.music.play(loops=1)
                                    pygame.mixer.Sound("explosion.wav").play()

            self.show_message(str(self.energy_released))

                        

            # Display everything
            pygame.display.update()

    def stop(self):
        pygame.quit()

    
    def show_message(self, message):
        # print('showing text')
        #sets the font and color
        font=pygame.font.SysFont('timesnewroman',  60)
        green = 255, 165, 0
        text = font.render(message, True, green)
        textRect = text.get_rect()
        #puts the score at the center of the screen
        textRect.center = (50, 50)
        window.blit(text, textRect)
        pygame.display.flip()
        # time.sleep(3)
    






class Sprite(pygame.sprite.Sprite):

    def __init__(self, sprite_x, sprite_y, width, sprite_position, name, type, energy):
        pygame.sprite.Sprite.__init__(self)
        self.sprite_x = sprite_x
        self.sprite_y = sprite_y
        self.texture = pygame.image.load('sprites.png')
        self.rect = pygame.Rect(width, sprite_position * width, width, width)
        self.direction_x = 1
        self.direction_y = 1
        self.width = width
        self.name = name
        self.type = type
        self.energy = 1
        self.killed = False


    def load(self):
        self.draw()

    def draw(self):
        location = pygame.math.Vector2(self.sprite_x, self.sprite_y)
        if self.killed == False:
            # pygame.draw.rect(window, (255,0,0), [0, 0, self.width, self.width], 1)
            window.blit(self.texture, location, self.rect)

    # Move on x axis primitive
    def move_x(self, move_x):
        self.sprite_x += move_x

    # Move on y axis primitive
    def move_y(self, move_y):
        self.sprite_y += move_y

    def move(self):
        # X
        if self.sprite_x == 0:
            self.direction_x = 1
        if self.sprite_x == screen_width - self.width:
            self.direction_x = -1
            # Sometimes, change the y direction
            if (random.randint(0, 1000) % 2 == 0):
                self.direction_y = -1

        # add in the direction randomly
        if (random.randint(0, 1000) % 2 == 0):
            self.move_x(1 * self.direction_x)

        # Y
        if self.sprite_y == 0:
            self.direction_y = 1
        if self.sprite_y == screen_height - self.width:
            self.direction_y = -1
            # Sometimes, change the x direction
            if (random.randint(0, 1000) % 2 == 0):
                self.direction_x = -1

        # add in the direction randomly
        if (random.randint(0, 1000) % 3 == 0):
            self.move_y(1 * self.direction_y)


    def check_collision(self, other_sprite):
        if (self.sprite_x < other_sprite.sprite_x + other_sprite.width and
            self.sprite_x + self.width > other_sprite.sprite_x and
            self.sprite_y < other_sprite.sprite_y + other_sprite.width and
            self.sprite_y + self.width > other_sprite.sprite_y):
            print('COLLISION DETECTED BETWEEN', self.name, other_sprite.name)
            return True
        return False
    
    
    def __check_collision(self, other_sprite):
        x = self.sprite_x
        y = self.sprite_y
        _x = other_sprite.sprite_x
        _y = other_sprite.sprite_y
        if(
            # x is between _x and _x + width
            (x >= _x and x <= _x + other_sprite.width)
            # y is between _y and _y + height
            or (y >= _y and y <= _y + other_sprite.width)
          ):
            return True
        
        return False
    

    def check_and_change_direction(self, other_sprite):
        if self.check_collision(other_sprite) == True:
            if self.direction_x == -1 and self.direction_y == -1:
                self.direction_x = 1
                self.direction_y = 1
            elif self.direction_x == 1 and self.direction_y == 1:
                self.direction_x = -1
                self.direction_y = -1
            elif self.direction_x == -1 and self.direction_y == 1:
                self.direction_x = 1
                self.direction_y = -1
            elif self.direction_x == 1 and self.direction_y == -1:
                self.direction_x = -1
                self.direction_y = 1
            return True
        return False

    def kill_sprite(self):
        self.killed = True




# Tank sprite
class Tank(Sprite):

    def __init__(self, x, y, width, name):
        sprite_position = 0
        type = 'tank'
        Sprite.__init__(self, x, y, width, sprite_position, name, type, 0)




# Rocket sprite
class Rocket(Sprite):

    def __init__(self, x, y, width, name):
        sprite_position = 12
        type = 'rocket'
        Sprite.__init__(self, x, y, width, sprite_position, name, type, 0)




game = Game()
game.create_sprites()
game.render_frames()
game.stop()

