# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 12:10:00 2026

@author: aidyn
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

# MENU variables
background = pygame.image.load('Menu Screen (Template) (1).png')
background = pygame.transform.scale(background, (width, height))
font = pygame.font.SysFont('arialbd.ttf', 42)
rules_font = pygame.font.SysFont('arialbd.ttf', 60)

menu_options = ['Start', 'Quit']
index = 0
game_state = 'MENU'

# 3. Set up a clock to control frame rate
clock = pygame.time.Clock()
FPS = 120
HIGHLIGHT = (255, 255, 143)
ARROW = (253, 61, 181)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#ball location
balls = np.array([[0, -50, -100, -150, -200, -250, -300, -350, -400,
                  -450], [100, 100, 100, 100, 100, 100, 100, 100,
                  100, 100]])
# call with balls[0, x]

#possible positions
posxlist = [100, 300, 500, 700]

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

#Rules Screen
def rules_screen():
    check = True
    rules_txt = ['RULES:', 'USE ARROW KEYS FOR NAVIGATION',
                 'USE D, F, J, K IN GAME',
                 'PRESS ESC TO RETURN TO MENU',
                 'Press RETURN to proceed!']
    for index, text in enumerate(rules_txt):
        txt_render = rules_font.render(text, True, WHITE)
        txt_rect = txt_render.get_rect(center =(width//2, 40 + index * 80))
        # edit distances for better spacing
        screen.blit(txt_render, txt_rect)
    pygame.display.flip()
    while check:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:    
                    check = False       
       
#sprite setup/ group
all_sprites_group = pygame.sprite.Group
# 4. Game Loop
running = True
rules_screen()
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
        
        #%% Beginning of gameplay loop
        # redraw
        screen.fill(BLACK)
        
        for k in range(len(balls[0])):
            balls[0, k] += 1
                
            if balls[0, k] == -25:
                balls[1, k] = posxlist[random.randint(0, 3)]
                # randomly choose from the list of possible positions
        
            if balls[0, k] == height + 25:
                balls[0, k] = -25
                
            pygame.draw.rect(screen, WHITE, (balls[1, k], balls[0, k], 20, 20))
        
        #(x, y, xsize, ysize)
        
        # all_sprites_group.update()
    
        # # Fill the background with a color (e.g., dark gray)
        # screen.fill(BLACK)
    
        # # Update the display
    pygame.display.flip()
    clock.tick(FPS)
  #%%  



# 5. Properly quit Pygame and exit
pygame.quit()