#!/usr/bin/env python3

import pygame
import sys
import random

# Initialise PyGame
pygame.init()
clock = pygame.time.Clock()

# Dimensions de la fenêtre
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

# Couleurs
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)
GRAY = (100, 100, 100) 

# Création de la fenêtre
fenetre = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("High School Escape Quest")

# Font
font_path = "retro-gaming-fonts.ttf"  # Replace with the path to your font file
font_size = 24
retro_font = pygame.font.Font(font_path, font_size)

# Variables pour maintenir l'état de la navigation dans le jeu
START_STATE = 'start'
MENU_STATE = 'menu'
MEMORY_STATE = 'memory'
TIC_TAC_TOE_STATE = 'tic_tac_toe'
QUIZ_STATE = 'quiz'

# Etat initial
state = START_STATE

# Fonds
menu_background = pygame.image.load("./images/plan_lycee.png").convert()
memory_background = pygame.image.load("./images/salle_memo.png").convert()
tic_tac_toe_background = pygame.image.load("./images/salle_morpion.png").convert()
quiz_background = pygame.image.load("./images/salle_quiz.png").convert()

# Boutons et Zones de clic
play_button_image = pygame.image.load("./images/bouton_play.png").convert_alpha()
play_button_image = pygame.transform.scale(play_button_image, (100,100))
play_button_pos = (250, 450)
play_button_rect = play_button_image.get_rect(topleft=play_button_pos)

memo_button_rect = pygame.Rect(0, 50, 193, 256)
morpion_button_rect = pygame.Rect(0, 311, 193, 289)
quiz_button_rect = pygame.Rect(365, 250, 235, 350)

menu_button_size = 50
menu_button_margin = 10
menu_button_rect = pygame.Rect(WINDOW_WIDTH - menu_button_size - menu_button_margin, menu_button_margin,
                               menu_button_size, menu_button_size)
menu_button_color = GRAY

# Curseur
cursor_image = pygame.image.load("./images/curseur.png").convert_alpha()
cursor_image = pygame.transform.scale(cursor_image, (50,50))
pygame.mouse.set_visible(False) # cache le pointeur de la souris

# Variables globales spécifiques pour chaque jeu
memory_game_case = []
memory_game_case_clicked = []
memory_game_results = []

def start_screen():
    # Affiche la page d'accueil du jeu
    fenetre.fill(WHITE)  # Clear the screen
    fond = pygame.image.load("./images/menu.png").convert()
    fenetre.blit(fond, (0, 0))
    fenetre.blit(play_button_image, play_button_rect)
    gérer_curseur()

def menu_screen():
    # Display the menu screen
    fenetre.blit(menu_background, (0, 0))
    pygame.draw.rect(fenetre, WHITE, memo_button_rect, 2)
    pygame.draw.rect(fenetre, WHITE, morpion_button_rect, 2)
    pygame.draw.rect(fenetre, WHITE, quiz_button_rect, 2)

    # Highlight buttons when mouse is over them
    if memo_button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(fenetre, LIGHT_BLUE, memo_button_rect, 2)
    if morpion_button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(fenetre, LIGHT_BLUE, morpion_button_rect, 2)
    if quiz_button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(fenetre, LIGHT_BLUE, quiz_button_rect, 2)

    gérer_curseur()

# Function to draw the menu button
def menu_button():
    button_text_surface = retro_font.render("Menu", True, menu_button_color)
    button_text_rect = button_text_surface.get_rect(topright=(WINDOW_WIDTH - menu_button_margin, menu_button_margin))
    fenetre.blit(button_text_surface, button_text_rect)

def init_memory_game():
    global memory_game_case
    global memory_game_results

    # Initilise le mémo s'il ne l'est pas déjà
    if not memory_game_case:
        # Dimensions des cases du mémo
        RECT_WIDTH = 70
        RECT_HEIGHT = 90
        GAP = 30  # Espace entre les rectangles

        # Calcul total de l'espace horizontal et vertical
        total_width = 4 * (RECT_WIDTH + GAP) - GAP
        total_height = 4 * (RECT_HEIGHT + GAP) - GAP

        # Position du coin supérieur gauche de la zone des rectangle
        start_x = (WINDOW_WIDTH - total_width) // 2
        start_y = (WINDOW_HEIGHT - total_height) // 2

        # Création des cases du mémo
        rect_positions  = []
        for ligne in range(3):
            for colonne in range(4):
                rect_positions.append((start_x + (RECT_WIDTH + GAP) * colonne + GAP,
                                       start_y + (RECT_HEIGHT + GAP) * ligne + GAP))

        # Mélanges les paires d'images
        index_images_disponibles = random.sample(list(range(6)) * 2, k=len(rect_positions))

        # Combine (zip) les index d'images et les cases du jeu
        memory_game_case = [{'rectangle': pygame.Rect(position[0], position[1], RECT_WIDTH, RECT_HEIGHT),
                             'image_index': image_index, 'clicked': False}
                            for position, image_index in zip(rect_positions, index_images_disponibles)]
        memory_game_results = []
 
def memory_game():
    global memory_game_case_clicked
    global state

    # Affiche le jeu mémo
    fenetre.blit(memory_background, (0, 0))
    menu_button()

    init_memory_game()

    # On itére sur l'ensemble des cases
    for rect_info in memory_game_case:
        # On affiche une case blanche si la case n'est pas déjà cliquées ou validées
        if rect_info not in memory_game_results and rect_info not in memory_game_case_clicked:
            rect_surf = pygame.Surface(rect_info['rectangle'].size)
            rect_surf.fill(WHITE)
            fenetre.blit(rect_surf, rect_info['rectangle'])

        # On révéle les cases cliquées ou validées
        if rect_info in memory_game_results or rect_info in memory_game_case_clicked:
            index = rect_info['image_index'] + 1
            image = pygame.image.load(f'./images/mémo/card_{index}.jpeg')
            image = pygame.transform.scale(image, (70, 90))
            fenetre.blit(image, rect_info['rectangle'])

    if len(memory_game_case_clicked) == 2: 
        pygame.display.update(memory_game_case_clicked[1]['rectangle'])

    gérer_curseur()

    # On teste si une paire de carte a été retournée
    if len(memory_game_case_clicked) == 2:
        print('compare ' + str(memory_game_case_clicked[0]) + ' à ' + str(memory_game_case_clicked[1]))
        # Si la paire est incorrecte, on doit à nouveau cacher les cartes
        if memory_game_case_clicked[0]['image_index'] != memory_game_case_clicked[1]['image_index']:
            print('wrong')
            pygame.time.delay(1000)
            for rect_info in memory_game_case_clicked:
                rect_info['clicked'] = False
        else:
            print('match')
            memory_game_results.extend(memory_game_case_clicked)

        # On réinitialise la liste des cartes cliquées
        memory_game_case_clicked.clear()

    # Check if all images are revealed
    if len(memory_game_results) == len(memory_game_case):
        print('memo complet')
        state = MENU_STATE  # Return to the menu screen after completing the memory game    

def tic_tac_toe_game():
    # Play the tic-tac-toe game
    fenetre.blit(tic_tac_toe_background, (0, 0))
    menu_button()
    # Implement tic-tac-toe game logic here
    gérer_curseur()

def quiz_game():
    # Play the quiz game
    fenetre.blit(quiz_background, (0, 0))
    menu_button()
    # Implement quiz game logic here
    gérer_curseur()

def gérer_curseur():
    # Display the cursor
    mouse_pos = pygame.mouse.get_pos()
    fenetre.blit(cursor_image, mouse_pos)

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
            # écran d'accueil
            if state == START_STATE and play_button_rect.collidepoint(event.pos):
                    state = MENU_STATE
          # écran menu
            elif state == MENU_STATE:
                if memo_button_rect.collidepoint(event.pos):
                    state = MEMORY_STATE
                elif morpion_button_rect.collidepoint(event.pos):
                    state = TIC_TAC_TOE_STATE
                elif quiz_button_rect.collidepoint(event.pos):
                    state = QUIZ_STATE
            elif state == MEMORY_STATE:
                # Gestion du bouton de retour au menu
                if menu_button_rect.collidepoint(event.pos):
                    state = MENU_STATE
                # On teste chaque case du mémo
                for rect_info in memory_game_case:
                    if rect_info['rectangle'].collidepoint(event.pos):
                        # Si ce n'est pas une case déjà cliquées ou validées, on l'ajoute à la liste des cases cliquées
                        if not rect_info['clicked'] and rect_info not in memory_game_results:
                            rect_info['clicked'] = True
                            memory_game_case_clicked.append(rect_info)                            
            elif state == TIC_TAC_TOE_STATE:
                # Gestion du bouton de retour au menu
                if menu_button_rect.collidepoint(event.pos):
                    state = MENU_STATE
            elif state == QUIZ_STATE:
                # Gestion du bouton de retour au menu
                if menu_button_rect.collidepoint(event.pos):
                    state = MENU_STATE

# Main game loop
while True:
    gérer_events()

    if state == START_STATE:
        start_screen()
    elif state == MENU_STATE:
        menu_screen()
    elif state == MEMORY_STATE:
        memory_game()
    elif state == TIC_TAC_TOE_STATE:
        tic_tac_toe_game()
    elif state == QUIZ_STATE:
        quiz_game()

    pygame.display.update()
    clock.tick(40)