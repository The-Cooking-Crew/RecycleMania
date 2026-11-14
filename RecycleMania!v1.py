# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 16:57:00 2026

@author: aidyn, eddie
"""

import pygame
import numpy as np
import random
import os

# 1. Initialize Pygame
pygame.init()

# 2. Set up the display window dimensions (width, height)
width, height = 800, 450
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("RecycleMania!")

# 3. Set up a clock to control frame rate
clock = pygame.time.Clock()
FPS = 120
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

font = pygame.font.Font(None, 48)

#ball location
balls = np.array([[-50, -100, -150, -200, -250, -300, -350, -400,
                  -450, -500], [100, 100, 100, 100, 100, 100, 100,
                   100, 100, 100]])
# call with balls[0, x]


#images
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

sprites = {
    "Bin closed": pygame.image.load(os.path.join(img_folder, "recyclebin1.jpg")),
    "Bin open": pygame.image.load(os.path.join(img_folder, "recyclebin2.jpg")),
    "balls": pygame.image.load(os.path.join(img_folder,"ball.png"))
    }
Bin_image = sprites["Bin closed"]
Ball_image = sprites["balls"]

Ball_image = pygame.transform.scale(Ball_image, (20,20))






#possible positions
posxlist = [100, 300, 500, 700]
for k in range(len(balls[0])):
    balls[1, k] = posxlist[random.randint(0, 3)]

deaths = 0
score = 0
buffered = {"d":False, "f":False, "j":False, "k":False}

#sprite setup/ group
all_sprites_group = pygame.sprite.Group
# 4. Game Loop
running = True
while running:
    # # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # redraw
    screen.fill(BLACK)
        
    # key value dictionary
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE] == True:
        Bin_image = sprites["Bin open"]
    else:
        Bin_image = sprites["Bin closed"]
    screen.blit(Bin_image,(100,100))
    pygame.draw.rect(screen, RED, (0, 300, 800, 20))
    pygame.draw.rect(screen, BLUE, (0, height - 10, 800, 20))
    screen.blit((font.render("Score: " + str(score), True, WHITE)),
                 (5, 5))
    screen.blit((font.render("Litters: " + str(deaths), True, WHITE)),
                 (400, 5))
    
    for k in range(len(balls[0])):
        balls[0, k] += 1
            
        if balls[0, k] == height - 30:
            deaths += 1
            score -= 1
        elif balls[0, k] == height + 25:
            balls[1, k] = posxlist[random.randint(0, 3)]
            # randomly choose from the list of possible positions
            balls[0, k] = -25
        elif balls[0, k] >= 280 and balls[0, k] <= 320:
            # ball in shooting range
            match balls[1, k]:
                case 100:
                    if keys[pygame.K_d] and not buffered["d"]:
                        balls[0, k] -= 500
                        score += 1
                case 300:
                    if keys[pygame.K_f] and not buffered["f"]:
                        balls[0, k] -= 500
                        score += 1
                case 500:
                    if keys[pygame.K_j] and not buffered["j"]:
                        balls[0, k] -= 500
                        score += 1
                case 700:
                    if keys[pygame.K_k] and not buffered["k"]:
                        balls[0, k] -= 500
                        score += 1
            
            
            pass
            
        screen.blit(Ball_image,(balls[1, k], balls[0, k]))
        

        #draw every ball
        #(x, y, xsize, ysize)
    
    

    buffered = {"d":keys[pygame.K_d], "f":keys[pygame.K_f],
                "j":keys[pygame.K_j], "k":keys[pygame.K_k]}
    # Makes sure player cannot buffer inputs.
    # Creates a boolean list of 4 (d, f, j, k, respectively)
    # where True is pressed and False is unpressed.
    # You can only score if the value for the letter is False
    # for the frame previous to the frame where you earn the point.
    # At this point, any taps now update so previously unpressed
    # keys update beyond this point and therefore do not get detected
    # earlier.

    # # Update the display:
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
#Quit application properly