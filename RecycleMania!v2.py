# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 12:10:00 2026

@author: eddie, aidyn, ray, yange
"""

import pygame
import numpy as np
import random

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



#ball location
balls = np.array([[-50, -100, -150, -200, -250, -300, -350, -400,
                  -450, -500], [0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
# call with balls[0, x]

# parts = np.array([[0.0, 0], [0, 0], [0, 0]])
# # first pair is if they exist
# # second pair is x
# # third pair is y

# def partrandom(parts, xlist, balls):
#     for k in range(1):
#         if parts[0, k] == 0:
#             parts[0, k] = 1
#             parts[1, k] = xlist[random.randint(0, 3)]
#             parts[2, k] = random.randint(-500, -50)


#possible positions
c1, c2, c3, c4 = 70.5, 177.5, 284, 391
posxlist = [c1, c2, c3, c4]
trashlist = [1, 1, 1, 2, 2, 3]
for k in range(len(balls[0])):
    balls[1, k] = posxlist[random.randint(0, 3)]
    balls[2, k] = trashlist[random.randint(0, 5)]

deaths = 0
score = 0
total = 0
partcount = 1
multiplier = 1
buffered = {"d":False, "f":False, "j":False, "k":False}



# images
gbackground = pygame.transform.scale(
    pygame.image.load('gp_bg.png'), (width, height))
dumpsteropen = pygame.transform.scale(
    pygame.image.load('Dumpster Open.png'), (width, height))
dumpsterclose = pygame.transform.scale(
    pygame.image.load('Dumpster Closed.png'), (width, height))
garb1 = pygame.transform.scale(
    pygame.image.load('garbage1.png'), (width, height))
garb2 = pygame.transform.scale(
    pygame.image.load('garbage2.png'), (width, height))
garb3 = pygame.transform.scale(
    pygame.image.load('garbage3.png'), (width, height))


# MENU variables
mbackground = pygame.image.load('menuscreen.png')
mbackground = pygame.transform.scale(mbackground, (width, height))
font = pygame.font.SysFont('arialbd.ttf', 42)
fontsmall = pygame.font.SysFont('arialbd.ttf', 20)

menu_options = ['Start', 'Quit']
index = 0
game_state = 'MENU'


#menu functions 
def make_menu():
    screen.blit(mbackground, (0, 0))
    for selected, option in enumerate(menu_options):
        if selected == index:
            color = ARROW
            label = "> %s <" %option
        else:
            color = BLACK
            label = option
        text_render = font.render(label, True, color)
        text_rect = text_render.get_rect(center=
            (695 + selected * 25, 232 + selected * 91))
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
        
        # set background
        screen.blit(gbackground, (0, 0))
        
        # key value dictionary
        keys = pygame.key.get_pressed()
        
        #adding rrecycle bins
        if keys[pygame.K_e] == True:
            screen.blit(pygame.transform.scale(dumpsteropen, (115,115)),
            (23,height-163))
        else:
            screen.blit(pygame.transform.scale(dumpsterclose,
            (115,115)),(23,height-163))
        
        if keys[pygame.K_r] == True:
            screen.blit(pygame.transform.scale(dumpsteropen,
            (115,115)),(127,height-163))
        else:
            screen.blit(pygame.transform.scale(dumpsterclose,
            (115,115)),(127,height-163))
        
        if keys[pygame.K_u] == True:
            screen.blit(pygame.transform.scale(dumpsteropen, (115,115)),
            (234,height-163))
        else:
            screen.blit(pygame.transform.scale(dumpsterclose,
            (115,115)),(234,height-163))
        
        if keys[pygame.K_i] == True:
            screen.blit(pygame.transform.scale(dumpsteropen, (115,115)),
            (341,height-163))
        else:
            screen.blit(pygame.transform.scale(dumpsterclose, (115,115)),
            (341,height-163))
        
        # pygame.draw.rect(screen, RED, (0, 302, 427, 20))
        # pygame.draw.rect(screen, BLUE, (0, height - 10, 425, 20))
        screen.blit((font.render("Score: " + str(int(score)), True,
                     WHITE)), (579, 298))
        screen.blit((font.render("Score: " + str(int(score)), True,
                     BLACK)), (580, 300))
        if deaths == 0:
            screen.blit((fontsmall.render("Accuracy: 100%",
                        True, WHITE)), (490, 5))
        else:
            screen.blit((fontsmall.render("Accuracy: " + str(
                    round(100 * (total - deaths) / total , 2)) + "%",
                    True, WHITE)), (490, 5))
        
        for k in range(len(balls[0])):
            balls[0, k] += 1
                
            if balls[0, k] == height - 30:
                deaths += 1
                total += 1
            elif balls[0, k] >= height + 1:
                balls[0, k] -= 500
            elif balls[0, k] >= 282 and balls[0, k] <= 322:
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
                    score += 1 * multiplier
                    total += 1
                
            elif balls[0, k] == -40:         
                balls[1, k] = posxlist[random.randint(0, 3)]
                balls[2, k] = trashlist[random.randint(0, 5)]
                # randomly choose from the list of possible positions
                

            if balls[2, k] == 1:
                screen.blit(pygame.transform.scale(garb1, (30, 30)),
                (balls[1, k] - 5, balls[0, k] - 5))
            elif balls[2, k] == 2:
                screen.blit(pygame.transform.scale(garb2, (32, 32)),
                (balls[1, k] - 8, balls[0, k] - 6))
            elif balls[2, k] == 3:
                screen.blit(pygame.transform.scale(garb3, (36, 36)),
                (balls[1, k] - 8, balls[0, k] - 8))
            
            
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
