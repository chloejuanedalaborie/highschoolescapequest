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
tic_tac_toe_background = pygame.image.load("./images/salle_morpion.png").convert()
tic_tac_toe_background = pygame.transform.scale(tic_tac_toe_background, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Boutons et Zones de clic
play_button_image = pygame.image.load("./images/bouton_play.png").convert_alpha()
play_button_image = pygame.transform.scale(play_button_image, (100,100))
play_button_pos = (250, 450)
play_button_rect = play_button_image.get_rect(topleft=play_button_pos)

# Curseur
cursor_image = pygame.image.load("./images/curseur.png").convert_alpha()
cursor_image = pygame.transform.scale(cursor_image, (50,50))
cursor_image_rect = cursor_image.get_rect()
pygame.mouse.set_visible(False) # cache le pointeur de la souris

def start_screen():
    # Affiche la page d'accueil du jeu
    fenetre.blit(title_screen_background, (0, 0))
    fenetre.blit(play_button_image, play_button_rect)

 

tictactoe_game_case = []
def init_tic_tac_toe_game():
    global tictactoe_game_case
    global tictactoe_game_player_turn  
        
    # Initilise le tictactoe s'il ne l'est pas déjà
    if not tictactoe_game_case:
 
        # Play the tic-tac-toe game
        fenetre.blit(tic_tac_toe_background, (0, 0))

        print('coucou')
        # Dimensions des cases du tictactoe
        SQUARE_WIDTH = 105
        SQUARE_HEIGHT = 105
        GAP = 30  # Espace entre les rectangles

        # Calcul total de l'espace horizontal et vertical
        total_width = 3 * (SQUARE_WIDTH + GAP) - GAP
        total_height = 3 * (SQUARE_HEIGHT + GAP) - GAP

        # Position du coin supérieur gauche de la zone des rectangle
        start_x = ((tic_tac_toe_background.get_width() - total_width) // 2) - (SQUARE_WIDTH // 4)
        start_y = ((tic_tac_toe_background.get_height() - total_height) // 2) + (SQUARE_HEIGHT // 4)

        # Création des cases du morpion
        tictactoe_game_case = []
        for ligne in range(3):
            for colonne in range(3):
                rect = pygame.Rect(start_x + (SQUARE_WIDTH + GAP) * colonne + GAP,
                                   start_y + (SQUARE_HEIGHT + GAP) * ligne + GAP, 
                                   SQUARE_WIDTH, 
                                   SQUARE_HEIGHT)
                surf = pygame.Surface(rect.size)
                surf.fill(pygame.Color('white'))
                fenetre.blit(surf, rect)
                tictactoe_game_case.append({'square': rect,'clicked': None})

                
        # Choisi aléatoirement qui commence la partie
        tictactoe_game_player_turn = random.choice([True,False])

def tic_tac_toe_game():
    global tictactoe_game_case
    global tictactoe_game_player_turn
    global state

    init_tic_tac_toe_game()

    """ if not tictactoe_game_player_turn:
        empty_square_case = random.choice([position for position in tictactoe_game_case if not position['clicked']])
        empty_square_case['clicked'] = 'computer'
        tictactoe_game_player_turn = True
                
    for square_info in tictactoe_game_case:
        square_surf = pygame.Surface(square_info['square'].size)
        # On affiche une case blanche si la case n'est pas déjà cliquées ou validées
        if not square_info['clicked']:
            square_surf.fill(pygame.Color('white'))
        elif 'player' in square_info['clicked']:
            square_surf.fill(pygame.Color('green'))
            #pygame.time.delay(2000)
        elif 'computer' in square_info['clicked']:
            square_surf.fill(pygame.Color('red'))

        fenetre.blit(square_surf, square_info['square']) """

def gérer_curseur():
    # Display the cursor
    cursor_image_rect.center = pygame.mouse.get_pos()
    fenetre.blit(cursor_image, cursor_image_rect)

def title_screen_events(mousePosition):
    global play_button_rect
    global state

    # Gestion du bouton de retour au menu
    if play_button_rect.collidepoint(mousePosition):
        state = TIC_TAC_TOE_STATE

def tictactoe_game_events(mousePosition):
    global tictactoe_game_case
    global tictactoe_game_player_turn
    global state
        
    # On teste chaque case du tictactoe
    for square_info in tictactoe_game_case:
        if square_info['square'].collidepoint(mousePosition):
            # Si ce n'est pas une case déjà cliquées
            if not square_info['clicked']:
                square_info['clicked'] = 'player'
                tictactoe_game_player_turn = False

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
                title_screen_events(event.pos)
            elif state == TIC_TAC_TOE_STATE:
                tictactoe_game_events(event.pos)

# Main game loop
while True:

    gérer_events()
    
    if state == START_STATE:
        start_screen()
    elif state == TIC_TAC_TOE_STATE:
        tic_tac_toe_game()

    gérer_curseur() 
    pygame.display.update()
    clock.tick(60)
