#!/usr/bin/env python3

import pygame
import sys
import random

# Initialise PyGame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('./musics/password-infinity-123276.mp3')
#pygame.mixer.music.play()
clock = pygame.time.Clock()

# Dimensions de la fenêtre
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

# Couleurs
TRANSPARENT = (0, 0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)
GRAY = (100, 100, 100)

# Création de la fenêtre
fenetre = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("High School Escape Quest")

# Font
font_path = "retro-gaming-fonts.ttf"

# Variables pour maintenir l'état de la navigation dans le jeu
START_STATE = 'start'
MENU_STATE = 'menu'
MEMORY_STATE = 'memory'
TIC_TAC_TOE_STATE = 'tic_tac_toe'
QUIZ_STATE = 'quiz'

# Etat initial
state = START_STATE

# Fonds
title_screen_background = pygame.image.load("./images/title.png").convert()
title_screen_background = pygame.transform.scale(title_screen_background, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Boutons et Zones de clic
play_button_image = pygame.image.load("./images/bouton_play.png").convert_alpha()
play_button_image = pygame.transform.scale(play_button_image, (100,100))
play_button_pos = (250, 450)
play_button_rect = play_button_image.get_rect(topleft=play_button_pos)

# Curseur
cursor_image = pygame.image.load("./images/curseur.png").convert_alpha()
cursor_image = pygame.transform.scale(cursor_image, (50,50))
pygame.mouse.set_visible(False) # cache le pointeur de la souris

def start_screen():
    # Affiche la page d'accueil du jeu
    fenetre.blit(title_screen_background, (0, 0))
    fenetre.blit(play_button_image, play_button_rect)
    gérer_curseur()

def gérer_curseur():
    # Display the cursor
    mouse_pos = pygame.mouse.get_pos()
    fenetre.blit(cursor_image, mouse_pos)

def title_screen_events(mousePosition):
    global play_button_rect
    global state

    # Gestion du bouton de retour au menu
    if play_button_rect.collidepoint(mousePosition):
        state = MENU_STATE

def gérer_events():
    # Handle events such as quitting and button clicks
    global state

    for event in pygame.event.get():
        # Quitter le jeu
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Gestion du clic
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if state == START_STATE:
                title_screen_events()
            """ elif state == MENU_STATE:
                menu_events(event.pos)
            elif state == MEMORY_STATE:
                memory_game_events(event.pos)
            elif state == TIC_TAC_TOE_STATE:
                morpion_game_events(event.pos)
            elif state == QUIZ_STATE:
                quiz_game_events(event.pos) """

# Main game loop
while True:

    gérer_events()

    fenetre.fill(WHITE)  # Clear the screen

    if state == START_STATE:
        start_screen()
    """ elif state == MENU_STATE:
        menu_screen()
    elif state == MEMORY_STATE:
        memory_game()
    elif state == TIC_TAC_TOE_STATE:
        tic_tac_toe_game()
    elif state == QUIZ_STATE:
        quiz_game() """

    pygame.display.update()
    clock.tick(60)
