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

# Nombre de vies du joueur au début la partie
LIVES = 3
life_image = pygame.image.load("./images/life.png").convert_alpha()
live_image = pygame.transform.scale(life_image, (15,15))
livesCount=LIVES

# Barre de score
score_barre_rect = pygame.Rect(0, 0, WINDOW_WIDTH, 50)

# Fonds
menu_background = pygame.image.load("./images/plan_lycee.png").convert()
memory_background = pygame.image.load("./images/salle_memo.png").convert()
memory_background = pygame.transform.scale(memory_background, (WINDOW_WIDTH, WINDOW_HEIGHT - score_barre_rect.height))
tic_tac_toe_background = pygame.image.load("./images/salle_morpion.png").convert()
tic_tac_toe_background = pygame.transform.scale(tic_tac_toe_background, (WINDOW_WIDTH, WINDOW_HEIGHT - score_barre_rect.height))
quiz_background = pygame.image.load("./images/salle_quiz.png").convert()
quiz_background = pygame.transform.scale(quiz_background, (WINDOW_WIDTH, WINDOW_HEIGHT - score_barre_rect.height))

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

# Curseur
cursor_image = pygame.image.load("./images/curseur.png").convert_alpha()
cursor_image = pygame.transform.scale(cursor_image, (50,50))
pygame.mouse.set_visible(False) # cache le pointeur de la souris

# Variables globales spécifiques pour chaque jeu
memory_game_case = []
memory_game_case_clicked = []
memory_game_results = []
memory_game_click_count = 0

final_memory_game_click_count = 0

def start_screen():
    # Affiche la page d'accueil du jeu
    fenetre.fill(WHITE)  # Clear the screen
    fond = pygame.image.load("./images/menu.png").convert()
    fenetre.blit(fond, (0, 0))
    fenetre.blit(play_button_image, play_button_rect)
    gérer_curseur()

def score_barre(bShowMenuButton=False, sScoreText=""):
    # Affiche la barre de score
    pygame.draw.rect(fenetre, WHITE, score_barre_rect, 0)
    score_text_font = pygame.font.Font(font_path, 12)

    life_text_surface = score_text_font.render("Vies :", True, GRAY)
    life_text_rect = life_text_surface.get_rect(topleft=(10, 10))
    fenetre.blit(life_text_surface, life_text_rect)
    for life in range(livesCount):
        fenetre.blit(live_image, (life_text_rect.width + (20 * life) + live_image.get_width() , 10))

    score_text_surface = score_text_font.render(sScoreText, True, GRAY)
    score_text_rect = score_text_surface.get_rect(topleft=(10, 30))
    fenetre.blit(score_text_surface, score_text_rect)

    if bShowMenuButton:
        # Affiche le bouton menu
        menu_button()

def menu_screen():
    global final_memory_game_click_count

    gameover_font = pygame.font.Font(font_path, 48)

    # Display the menu screen
    fenetre.blit(menu_background, (0, 0))
    score_barre()

    memo_image_text_font = pygame.font.Font(font_path, 24)
    memo_image_text_surface = memo_image_text_font.render("Mémo", True, pygame.Color('black'))
    memo_rect = pygame.draw.rect(fenetre, WHITE, memo_button_rect, 2)
    memo_image = pygame.transform.scale(memory_background, memo_rect.size)
    memo_image_text_rect = memo_image_text_surface.get_rect(center=memo_image.get_rect().center)
    memo_image.blit(memo_image_text_surface, memo_image_text_rect)
    fenetre.blit(memo_image, memo_rect)
    # Vérifier si le score est supérieur à 0
    if final_memory_game_click_count > 0:
        # Afficher le score centré en bas du bouton mémo
        score_font = pygame.font.Font(font_path, 18)
        score_text = "Score: " + str(final_memory_game_click_count)
        score_text_surface = score_font.render(score_text, True, pygame.Color('green'))
        score_text_rect = score_text_surface.get_rect(center=(memo_button_rect.centerx, memo_button_rect.bottom - 50))
        fenetre.blit(score_text_surface, score_text_rect)

    morpion_image_text_font = pygame.font.Font(font_path, 24)
    morpion_image_text_surface = morpion_image_text_font.render("Morpion", True, pygame.Color('black'))
    morpion_rect = pygame.draw.rect(fenetre, WHITE, morpion_button_rect, 2)
    morpion_image = pygame.transform.scale(tic_tac_toe_background, morpion_rect.size)
    morpion_image_text_rect = morpion_image_text_surface.get_rect(center=morpion_image.get_rect().center)
    morpion_image.blit(morpion_image_text_surface, morpion_image_text_rect)
    fenetre.blit(morpion_image, morpion_rect)

    quiz_image_text_font = pygame.font.Font(font_path, 24)
    quiz_image_text_surface = quiz_image_text_font.render("Quiz", True, pygame.Color('black'))
    quiz_rect = pygame.draw.rect(fenetre, WHITE, quiz_button_rect, 2)
    quiz_image = pygame.transform.scale(quiz_background, quiz_rect.size)
    quiz_image_text_rect = quiz_image_text_surface.get_rect(center=quiz_image.get_rect().center)
    quiz_image.blit(quiz_image_text_surface, quiz_image_text_rect)
    fenetre.blit(quiz_image, quiz_rect)

    # Highlight buttons when mouse is over them
    if memo_button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(fenetre, LIGHT_BLUE, memo_button_rect, 2)
    if morpion_button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(fenetre, LIGHT_BLUE, morpion_button_rect, 2)
    if quiz_button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(fenetre, LIGHT_BLUE, quiz_button_rect, 2)

    # Afficher "Game Over !" quand le joeur n'a plus de vie
    if livesCount == 0:
        complete_text_surface = gameover_font.render("Game Over !", True, pygame.Color('red'))
        complete_text_rect = complete_text_surface.get_rect(center=(WINDOW_WIDTH // 2, 30))
        fenetre.blit(complete_text_surface, complete_text_rect)

    gérer_curseur()

# Function to draw the menu button
def menu_button():
    menu_font = pygame.font.Font(font_path, 24)
    button_text_surface = menu_font.render("Menu", True, GRAY)
    button_text_rect = button_text_surface.get_rect(topright=(WINDOW_WIDTH - menu_button_margin, menu_button_margin))
    fenetre.blit(button_text_surface, button_text_rect)
    if button_text_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(fenetre, LIGHT_BLUE, button_text_rect, 2)

def init_memory_game():
    global memory_game_case
    global memory_game_results
    global memory_game_click_count
    global livesCount

    # Initilise le mémo s'il ne l'est pas déjà
    if not memory_game_case and livesCount > 0:
        print("initialisation du mémo")
        memory_game_click_count = 0

        # Dimensions des cases du mémo
        RECT_WIDTH = 105
        RECT_HEIGHT = 125
        GAP = 30  # Espace entre les rectangles

        # Calcul total de l'espace horizontal et vertical
        total_width = 4 * (RECT_WIDTH + GAP) - GAP
        total_height = 3 * (RECT_HEIGHT + GAP) - GAP

        # Position du coin supérieur gauche de la zone des rectangle
        start_x = ((memory_background.get_width() - total_width) // 2) - (RECT_WIDTH // 4)
        start_y = ((memory_background.get_height() - total_height) // 2) + (RECT_HEIGHT // 4)
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
    global memory_game_click_count
    global memory_game_case
    global state
    global livesCount
    global final_memory_game_click_count

    MAX_TENTATIVES=10

    # Affiche le jeu mémo
    fenetre.blit(memory_background, (0, score_barre_rect.height))

    gameover_font = pygame.font.Font(font_path, 48)

    # Affiche la barre de score
    score_barre(True, "Nombre de tentatives: " + str(memory_game_click_count))

    init_memory_game()

    # On itére sur l'ensemble des cases
    for rect_info in memory_game_case:
        # On affiche une case blanche si la case n'est pas déjà cliquées ou validées
        if rect_info not in memory_game_results and rect_info not in memory_game_case_clicked:
            rect_surf = pygame.Surface(rect_info['rectangle'].size)
            rect_surf.fill(pygame.Color('white'))
            fenetre.blit(rect_surf, rect_info['rectangle'])

        # On révéle les cases cliquées ou validées
        if rect_info in memory_game_results or rect_info in memory_game_case_clicked:
            index = rect_info['image_index'] + 1
            image = pygame.image.load(f'./images/mémo/card_{index}.jpeg')
            image = pygame.transform.scale(image, (105, 125))
            fenetre.blit(image, rect_info['rectangle'])

    gérer_curseur()

    # On teste si une paire de carte a été retournée
    if len(memory_game_case_clicked) == 2:
        memory_game_click_count += 1
        # Si la paire est incorrecte, on doit à nouveau cacher les cartes
        if memory_game_case_clicked[0]['image_index'] != memory_game_case_clicked[1]['image_index']:
            # on force la mise à jour de l'affichage pour laisser le temps au joueur de voir la carte
            pygame.display.update(memory_game_case_clicked[1]['rectangle'])
            pygame.time.delay(1000)
            for rect_info in memory_game_case_clicked:
                rect_info['clicked'] = False
        else:
            # on ajoute la paire aux cartes validées
            memory_game_results.extend(memory_game_case_clicked)

        # On réinitialise la liste des cartes cliquées
        memory_game_case_clicked.clear()

    if memory_game_click_count >= MAX_TENTATIVES or len(memory_game_results) == len(memory_game_case):
        # On conserve le score final pour l'affichage sur le menu
        final_memory_game_click_count = memory_game_click_count

        # Au delà de 10 tentatives on perd une vie et on retourne au menu
        if memory_game_click_count >= MAX_TENTATIVES:
            gameover_color= pygame.Color('red')
            gameover_text = "Perdu !"
            # S'il reste au moins 1 vie au joueur on réinitialise le mémo
            if livesCount > 0:
                livesCount -= 1
                memory_game_results.clear()
                memory_game_case_clicked.clear()
                if livesCount > 1:
                    memory_game_case.clear()

        # Si toutes les cartes ont été retournées, le jeu est fini on retourne au menu
        elif len(memory_game_results) == len(memory_game_case):
            gameover_color= pygame.Color('green')
            gameover_text = "Well done !"

        # Afficher "Perdu !" ou  "Well done !"
        print("Mémo gameover: " + gameover_text)
        complete_text_surface = gameover_font.render(gameover_text, True, gameover_color)
        complete_text_rect = complete_text_surface.get_rect(center=(WINDOW_WIDTH // 2, 30))
        fenetre.blit(complete_text_surface, complete_text_rect)

        # Afficher toutes les cases la couleur perdu ou gagné
        for rect_info in memory_game_case:
            rect_surf = pygame.Surface(rect_info['rectangle'].size)
            rect_surf.fill(gameover_color)
            fenetre.blit(rect_surf, rect_info['rectangle'])
            pygame.draw.rect(fenetre, WHITE, rect_info['rectangle'], 2)

        pygame.display.update()
        pygame.time.delay(2000)

        state = MENU_STATE

def tic_tac_toe_game():
    # Play the tic-tac-toe game
    fenetre.blit(tic_tac_toe_background, (0, score_barre_rect.height))

    # Affiche la barre de score
    score_barre(True)

    # Implement tic-tac-toe game logic here
    gérer_curseur()

def quiz_game():
    # Play the quiz game
    fenetre.blit(quiz_background, (0, score_barre_rect.height))

    # Affiche la barre de score
    score_barre(True)

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
    clock.tick(60)