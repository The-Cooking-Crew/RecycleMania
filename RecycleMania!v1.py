# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 12:10:00 2026

@author: eddie, aidyn, ray, yange
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
HIGHLIGHT = (255, 255, 143)
ARROW = (253, 61, 181)

font = pygame.font.Font(None, 48)


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


#ball location
balls = np.array([[-50, -100, -150, -200, -250, -300, -350, -400,
                  -450, -500], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
# call with balls[0, x]


#possible positions
c1, c2, c3, c4 = 100, 175, 250, 325
posxlist = [c1, c2, c3, c4]
for k in range(len(balls[0])):
    balls[1, k] = posxlist[random.randint(0, 3)]

deaths = 0
score = 0
total = 0
buffered = {"d":False, "f":False, "j":False, "k":False}


# MENU variables
background = pygame.image.load('menuscreen.png')
background = pygame.transform.scale(background, (width, height))
font = pygame.font.SysFont('arialbd.ttf', 42)

menu_options = ['Start', 'Quit']
index = 0
game_state = 'MENU'


#menu functions 
def make_menu():
    screen.blit(background, (0, 0))
    for selected, option in enumerate(menu_options):
        if selected == index:
            color = ARROW
            label = "> %s <" %option
        else:
            color = BLACK
            label = option
        text_render = font.render(label, True, color)
        text_rect = text_render.get_rect(center=(695 + selected * 25, 232 + selected * 91))
        screen.blit(text_render, text_rect)
    

def select_option(index, menu_options):
    global game_state
    option = menu_options[index]
    if option == 'Start':
        game_state = 'PLAY'
    elif option == 'Quit':
       global running
       running = False


#sprite setup/ group
all_sprites_group = pygame.sprite.Group

# 4. Game Loop
running = True
while running:
    # # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if game_state == 'MENU':
                if event.key == pygame.K_UP:
                    index = (index - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    index = (index + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    select_option(index, menu_options)
            elif event.key == pygame.K_ESCAPE:
                game_state = 'MENU'
    
    if game_state == "MENU":
        make_menu()
    elif game_state == "PLAY":
                        
        # redraw
        screen.fill(BLACK)
            
        # key value dictionary
        keys = pygame.key.get_pressed()
        
        pygame.draw.rect(screen, RED, (0, 300, 425, 20))
        pygame.draw.rect(screen, BLUE, (0, height - 10, 425, 20))
        screen.blit((font.render("Score: " + str(score), True, WHITE)),
                     (450, 5))
        screen.blit((font.render("Litters: " + str(deaths), True, WHITE)),
                     (450, 50))
        if deaths == 0:
            screen.blit((font.render("Accuracy: 100%",
                        True, WHITE)), (450, 95))
        else:
            screen.blit((font.render("Accuracy: " + str(
                    round(100 * (total - deaths) / total , 2)) + "%",
                    True, WHITE)), (450, 95))
        
        for k in range(len(balls[0])):
            balls[0, k] += 1
                
            if balls[0, k] == height - 30:
                deaths += 1
                score -= 1
                total += 1
            elif balls[0, k] >= height + 25:
                balls[0, k] -= 500
            elif balls[0, k] >= 280 and balls[0, k] <= 320:
                # ball in shooting range
                
                if (
                (balls[1, k] == c1 and
                keys[pygame.K_d] and not buffered["d"])
                or (balls[1, k] == c2 and
                keys[pygame.K_f] and not buffered["f"])
                or (balls[1, k] == c3 and
                keys[pygame.K_j] and not buffered["j"])
                or (balls[1, k] == c4 and
                keys[pygame.K_k] and not buffered["k"])
                ):
                    balls[0, k] -= 500
                    score += 1
                    total += 1
                
            elif balls[0, k] == -20:         
                balls[1, k] = posxlist[random.randint(0, 3)]
                # randomly choose from the list of possible positions
                
            pygame.draw.rect(screen, WHITE,
                            (balls[1, k], balls[0, k], 20, 20))
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
