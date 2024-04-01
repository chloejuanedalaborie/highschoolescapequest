#!/usr/bin/env python3

import pygame
import sys
import random

# Variables pour maintenir l'état de la navigation dans le jeu
START_STATE = 'start'
MENU_STATE = 'menu'
MEMORY_STATE = 'memory'
TIC_TAC_TOE_STATE = 'tic_tac_toe'
QUIZ_STATE = 'quiz'
END_STATE = 'game_over'

# Dimensions de la fenêtre
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

# Backgrounds
MENU_BACKGROUND_IMAGE = "./images/plan_lycee.png"
MEMORY_BACKGROUND_IMAGE = "./images/salle_memo.png"
TICTACTOE_BACKGROUND_IMAGE = "./images/salle_morpion.png"
QUIZ_BACKGROUND_IMAGE = "./images/salle_quiz.png"

# Zones de clics
MEMO_BUTTON_RECT = pygame.Rect(0, 50, 193, 256)
TICTACTOE_BUTTON_RECT = pygame.Rect(0, 311, 193, 289)
QUIZ_BUTTON_RECT = pygame.Rect(365, 250, 235, 350)

# Pointeur de souris
CURSOR_IMAGE = "./images/curseur.png"

# Fonts
GAME_FONTS = "./fonts/retro-gaming-fonts.ttf"

# Hauteur de la score-barre
SCORE_BARRE_HEIGHT = 50
SCORE_BARRE_MENU_BUTTON_SIZE = 50
SCORE_BARRE_MENU_BUTTON_MARGIN = 10
SCORE_BARRE_MENU_BUTTON_TEXT = "Menu"
SCORE_BARRE_LIFE_FULL_IMAGE = "./images/Icon_Large_HeartFull.png"
SCORE_BARRE_LIFE_EMPTY_IMAGE = "./images/Icon_Large_HeartEmpty.png"
SCORE_BARRE_LIFE_IMAGE_DIMENSIONS = (15, 15)

MAX_LIVES = 3
MEMORY_GAME_MAX_TENTATIVES = 10

def display_start_screen():
    # Affiche la page d'accueil du jeu
    fond = pygame.image.load("./images/title.png").convert()
    fond = pygame.transform.scale(fond, (WINDOW_WIDTH, WINDOW_HEIGHT))

    fenetre.blit(fond, (0, 0))

    # Charger l'image du bouton  
    start_button_image = pygame.image.load('./images/bouton_play.png').convert_alpha()
    start_button_image = pygame.transform.scale(start_button_image, (start_button_rect.width, start_button_rect.height))

    # Blitter le bouton sur l'écran
    fenetre.blit(start_button_image, start_button_rect)

def display_menu_screen():
    fenetre_surface = pygame.display.get_surface()
    
    # Fond d'écran
    menu_background = pygame.image.load(MENU_BACKGROUND_IMAGE).convert()
    menu_background = pygame.transform.scale(menu_background, (fenetre_surface.get_width(), fenetre_surface.get_height()))
    fenetre_surface.blit(menu_background, (0, 0))

    buttons = [
        {"image": MEMORY_BACKGROUND_IMAGE,
         "rect": MEMO_BUTTON_RECT,
         "text": "Mémo"},
        {"image": TICTACTOE_BACKGROUND_IMAGE,
         "rect": TICTACTOE_BUTTON_RECT,
         "text": "Morpion"},
        {"image": QUIZ_BACKGROUND_IMAGE,
         "rect": QUIZ_BUTTON_RECT,
         "text": "Quiz"}                  
    ]

    for button in buttons:
        # Charger l'image du bouton
        button_image = pygame.image.load(button["image"]).convert()

        # Dessiner le rectangle du bouton
        pygame.draw.rect(fenetre_surface, pygame.Color('white'), button["rect"], 2)

        # Mettre à l'échelle l'image pour qu'elle s'adapte à la taille du bouton
        button_image = pygame.transform.scale(button_image, button["rect"].size)

        # Ajouter du texte au bouton
        if button["text"] != "":
            text_font = pygame.font.Font(GAME_FONTS, 24)
            text_surface = text_font.render(button["text"], True, pygame.Color('black'))
            text_rect = text_surface.get_rect(center=button_image.get_rect().center)
            button_image.blit(text_surface, text_rect.topleft)

        # Blitter le bouton sur l'écran
        fenetre_surface.blit(button_image, button["rect"])

def display_score_barre(lives, bShowMenuButton=False, sScoreText="", dGameOverText={}):
    life_full_image = pygame.image.load(SCORE_BARRE_LIFE_FULL_IMAGE).convert_alpha()
    life_full_image = pygame.transform.scale(life_full_image, (15, 15))
    life_empty_image = pygame.image.load(SCORE_BARRE_LIFE_EMPTY_IMAGE).convert_alpha()
    life_empty_image = pygame.transform.scale(life_empty_image, (15, 15))    

    # Affiche la barre de score
    fenetre_surface = pygame.display.get_surface()
    score_barre_rect = pygame.Rect(0, 0, fenetre_surface.get_width(), SCORE_BARRE_HEIGHT)
    pygame.draw.rect(fenetre_surface, pygame.Color('white'), score_barre_rect, 0)

    # Vie: <lives>                                         |  Menu   |
    # <score_text>         < gameover_text >                    |  Button |

    score_text_font = pygame.font.Font(GAME_FONTS, 12)
    gameover_font = pygame.font.Font(GAME_FONTS, 48)

    # Affichage du nombre de vies
    life_text_surface = score_text_font.render("Vies :", True, pygame.Color('gray44'))
    life_text_rect = life_text_surface.get_rect(topleft=(10, 10))
    fenetre_surface.blit(life_text_surface, life_text_rect)
    for life_full in range(lives):
        fenetre_surface.blit(life_full_image, (life_text_rect.width + 20 + (life_full * life_full_image.get_width()), 10))
    for life_empty in range(MAX_LIVES - lives):
        fenetre_surface.blit(life_empty_image, (life_text_rect.width + 20 + (lives * (life_full_image.get_width())) + (life_empty * life_empty_image.get_width()), 10))

    # Affichage du score_text
    if sScoreText != "":
        score_text_surface = score_text_font.render(sScoreText, True, pygame.Color('gray44'))
        score_text_rect = score_text_surface.get_rect(topleft=(10, 30))
        fenetre_surface.blit(score_text_surface, score_text_rect)

        # Affichage du texte de fin de partie
        if dGameOverText:
            gameover_text_surface = gameover_font.render(dGameOverText['text'], True, dGameOverText['color'])
            gameover_text_rect = gameover_text_surface.get_rect(midleft=(score_text_rect.right + 20, 30)) # à décaler un peu à droite
            fenetre_surface.blit(gameover_text_surface, gameover_text_rect)

    if bShowMenuButton:
        menu_button_text_font = pygame.font.Font(GAME_FONTS, 24)
        menu_button_text_surface = menu_button_text_font.render(SCORE_BARRE_MENU_BUTTON_TEXT, True, pygame.Color('gray44'))
        menu_button_text_rect = menu_button_text_surface.get_rect(topright=(fenetre_surface.get_width() - SCORE_BARRE_MENU_BUTTON_SIZE, SCORE_BARRE_MENU_BUTTON_MARGIN))

        # Affiche le bouton menu
        fenetre_surface.blit(menu_button_text_surface, menu_button_text_rect)

        if menu_button_text_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(fenetre_surface, pygame.Color('lightblue'), menu_button_text_rect, 2)  

def initialize_memory_game():
    # Dimensions des cases du mémo
    RECT_WIDTH = 105
    RECT_HEIGHT = 125
    GAP = 30  # Espace entre les rectangles

    # Calcul total de l'espace horizontal et vertical
    total_width = 4 * (RECT_WIDTH + GAP) - GAP
    total_height = 3 * (RECT_HEIGHT + GAP) - GAP

    # Position du coin supérieur gauche de la zone des rectangle
    start_x = ((WINDOW_WIDTH - total_width) // 2) - (RECT_WIDTH // 4)
    start_y = ((WINDOW_HEIGHT - SCORE_BARRE_HEIGHT - total_height) // 2) + (RECT_HEIGHT // 4)

    # Création des cases du mémo
    rect_positions  = []
    for ligne in range(3):
        for colonne in range(4):
            rect_positions.append((start_x + (RECT_WIDTH + GAP) * colonne + GAP,
                                    start_y + (RECT_HEIGHT + GAP) * ligne + GAP))

    # Mélanges les paires d'images
    index_images_disponibles = random.sample(list(range(6)) * 2, k=len(rect_positions))

    # Combine (zip) les index d'images et les cases du jeu
    return [{'rectangle': pygame.Rect(position[0], position[1], RECT_WIDTH, RECT_HEIGHT),
             'image_index': image_index,
             'clicked': False}
            for position, image_index in zip(rect_positions, index_images_disponibles)]

def display_memory_game(cases, cases_selected, cases_found, memory_game_click_count):
    # Play the memory game
    fenetre_surface = pygame.display.get_surface()
    
    # Fond d'écran
    memory_background = pygame.image.load(MEMORY_BACKGROUND_IMAGE).convert()
    memory_background = pygame.transform.scale(memory_background, (fenetre_surface.get_width(), fenetre_surface.get_height() - SCORE_BARRE_HEIGHT))
    fenetre_surface.blit(memory_background, (0, SCORE_BARRE_HEIGHT))

    fenetre_surface = pygame.display.get_surface()

    # On itére sur l'ensemble des cases
    for rect_info in cases:
        index = rect_info['image_index'] + 1
        rect_surf = pygame.image.load(f'./images/mémo/card_{index}.jpeg').convert()
        rect_surf = pygame.transform.scale(rect_surf, (105, 125))        
      
        # Si le joueur a gagné, on met toutes les cases en vert
        if len(cases_found) == len(cases):
            rect_surf.fill(pygame.Color('green'))
        # Si le joueur a perdu, on met toutes les cases en rouge
        elif memory_game_click_count >= MEMORY_GAME_MAX_TENTATIVES:
            rect_surf.fill(pygame.Color('red'))
        # On affiche une case blanche si la case n'est pas déjà cliquées ou validées
        elif rect_info not in cases_found and rect_info not in cases_selected:
            rect_surf.fill(pygame.Color('white'))

        fenetre_surface.blit(rect_surf, rect_info['rectangle'])    

def initialize_tictactoe_game():
    print("Tic Tac Toe: initialisation")

    # Dimensions des cases du tictactoe
    SQUARE_WIDTH = 105
    SQUARE_HEIGHT = 105
    GAP = 30  # Espace entre les rectangles

    # Calcul total de l'espace horizontal et vertical
    total_width = 3 * (SQUARE_WIDTH + GAP) - GAP
    total_height = 3 * (SQUARE_HEIGHT + GAP) - GAP

    # Position du coin supérieur gauche de la zone des rectangle
    start_x = ((WINDOW_WIDTH - total_width) // 2) - (SQUARE_WIDTH // 4)
    start_y = ((WINDOW_HEIGHT - SCORE_BARRE_HEIGHT - total_height) // 2) + (SQUARE_HEIGHT // 4)

    # Création des cases du morpion
    tictactoe_game_case = []
    for ligne in range(3):
        for colonne in range(3):
            rect = pygame.Rect(start_x + (SQUARE_WIDTH + GAP) * colonne + GAP,
                                start_y + (SQUARE_HEIGHT + GAP) * ligne + GAP, 
                                SQUARE_WIDTH, 
                                SQUARE_HEIGHT)
            tictactoe_game_case.append({'square': rect,'clicked': None})

    return tictactoe_game_case

def check_tictactoe_game_over(cases):

    for i in range(3):
        # On test s'il y a une ligne compléte
        if cases[i * 3]['clicked'] == cases[i * 3 + 1]['clicked'] == cases[i * 3 + 2]['clicked'] is not None:
            return True, cases[i * 3]['clicked']
        # On test s'il y a une colonne compléte
        if cases[i]['clicked'] == cases[i + 3]['clicked'] == cases[i + 6]['clicked'] is not None:
            return True, cases[i]['clicked']

    # On test les 2 diagonales        
    if cases[0]['clicked'] == cases[4]['clicked'] == cases[8]['clicked'] is not None:
        return True, cases[0]['clicked']
    if cases[2]['clicked'] == cases[4]['clicked'] == cases[6]['clicked'] is not None:
        return True, cases[2]['clicked'] 

    return False, None

def display_tictactoe_game(cases):
    # Play the tictactoe game
    fenetre_surface = pygame.display.get_surface()
    
    # Fond d'écran
    tictactoe_background = pygame.image.load(TICTACTOE_BACKGROUND_IMAGE).convert()
    tictactoe_background = pygame.transform.scale(tictactoe_background, (fenetre_surface.get_width(), fenetre_surface.get_height() - SCORE_BARRE_HEIGHT))
    fenetre_surface.blit(tictactoe_background, (0, SCORE_BARRE_HEIGHT))

    text_font = pygame.font.Font(None, 92)
    
    for square_info in cases:
        square_surf = pygame.Surface(square_info['square'].size)

        # On affiche une case blanche
        square_surf.fill(pygame.Color('white'))
        fenetre_surface.blit(square_surf, square_info['square'])        
        
        if square_info['clicked']:
            if 'player' in square_info['clicked']:                
                text_surface = text_font.render("O", True, pygame.Color('blue'))
                text_rect = text_surface.get_rect(center=square_info['square'].center)
            elif 'computer' in square_info['clicked']:
                text_surface = text_font.render("X", True, pygame.Color('red'))
                text_rect = text_surface.get_rect(center=square_info['square'].center)
            fenetre_surface.blit(text_surface, text_rect.topleft) 

def run_quiz_game():
    fenetre_surface = pygame.display.get_surface()
    
    # Fond d'écran
    quiz_background = pygame.image.load(QUIZ_BACKGROUND_IMAGE).convert()
    quiz_background = pygame.transform.scale(quiz_background, (fenetre_surface.get_width(), fenetre_surface.get_height() - SCORE_BARRE_HEIGHT))
    fenetre_surface.blit(quiz_background, (0, SCORE_BARRE_HEIGHT))

def display_final_screen():
    # Affiche la page du gameover
    pass

# Remplace le curseur de la souris par une image
def display_cursor():
    pygame.mouse.set_visible(False) # cache le pointeur par défaut
    fenetre_surface = pygame.display.get_surface()

    cursor_surface = pygame.image.load(CURSOR_IMAGE).convert_alpha()
    cursor_surface = pygame.transform.scale(cursor_surface, (50, 50))

    coord = cursor_surface.get_rect()
    coord.center = pygame.mouse.get_pos()
    fenetre_surface.blit(cursor_surface, coord)

# Initialise PyGame
pygame.init()
clock = pygame.time.Clock()

# Initialise le mixer pour la musique et les sons
pygame.mixer.init()

pygame.mixer.music.load('./musics/password-infinity-123276.mp3')
pygame.mixer.music.play()

# Création de la fenêtre
fenetre = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("High School Escape Quest")

state = START_STATE
lives = MAX_LIVES
score = 0

start_button_rect = pygame.Rect(252, 450, 100, 100)

# Variables pour permettre d'ajouter du délai à l'affichage
playerDelayDisplayUpdate = 0
gameoverDelayDisplayUpdate = 0

# Variables Tic Tac Toe
tictactoe_game_cases = []
tictactoe_game_player_turn = None

# Variables Mémo
memory_game_cases = []
memory_game_cases_selected = []
memory_game_cases_found = []
memory_game_click_count = 0

# Main game loop
while True:
    fenetre_surface = pygame.display.get_surface()

    for event in pygame.event.get():
        # Quitter le jeu
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Gestion du clic
        elif event.type == pygame.MOUSEBUTTONDOWN:

            # écran d'accueil
            if state == START_STATE and start_button_rect.collidepoint(event.pos):
                state = MENU_STATE

            # écran menu
            elif state == MENU_STATE:
                if MEMO_BUTTON_RECT.collidepoint(event.pos):
                    print('Menu: le joueur a cliqué sur le jeu "mémo"')
                    pygame.draw.rect(fenetre_surface, pygame.Color('lightblue'), MEMO_BUTTON_RECT, 2)
                    state = MEMORY_STATE
                elif TICTACTOE_BUTTON_RECT.collidepoint(event.pos):
                    print('Menu: le joueur a cliqué sur le jeu "morpion"')
                    pygame.draw.rect(fenetre_surface, pygame.Color('lightblue'), TICTACTOE_BUTTON_RECT, 2)
                    state = TIC_TAC_TOE_STATE
                elif QUIZ_BUTTON_RECT.collidepoint(event.pos):
                    print('Menu: le joueur a cliqué sur le jeu "quiz"')
                    pygame.draw.rect(fenetre_surface, pygame.Color('lightblue'), QUIZ_BUTTON_RECT, 2)
                    state = QUIZ_STATE

            else:
                # Gestion du bouton de retour au menu de la score-barre
                menu_button_text_font = pygame.font.Font(GAME_FONTS, 24)
                menu_button_text_surface = menu_button_text_font.render(SCORE_BARRE_MENU_BUTTON_TEXT, True, pygame.Color('gray44'))
                menu_button_text_rect = menu_button_text_surface.get_rect(topright=(fenetre_surface.get_width() - SCORE_BARRE_MENU_BUTTON_SIZE, SCORE_BARRE_MENU_BUTTON_MARGIN))                
                if menu_button_text_rect.collidepoint(event.pos):
                    state = MENU_STATE

                if state == MEMORY_STATE:
                    if not memory_game_click_count >= MEMORY_GAME_MAX_TENTATIVES or not len(memory_game_cases_found) == len(memory_game_cases):
                        # On teste chaque case du mémo
                        for rect_info in memory_game_cases:
                            if rect_info['rectangle'].collidepoint(event.pos):
                                # Si ce n'est pas une case déjà cliquées ou validées, on l'ajoute à la liste des cases cliquées
                                if not rect_info['clicked'] and rect_info not in memory_game_cases_found and len(memory_game_cases_selected) < 2:
                                    rect_info['clicked'] = True
                                    memory_game_cases_selected.append(rect_info)

                                    # On teste si une paire de carte a été retournée
                                    if len(memory_game_cases_selected) == 2:
                                        # on incrémente le nombre de tentatives
                                        memory_game_click_count += 1

                                        # Si la paire est incorrecte, on doit à nouveau cacher les cartes
                                        if memory_game_cases_selected[0]['image_index'] != memory_game_cases_selected[1]['image_index']:
                                            # On initialise un delai pour laisser au joueur le temps de voir la carte
                                            print(f'Mémo: tentative #{memory_game_click_count}: paire KO')
                                            playerDelayDisplayUpdate = pygame.time.get_ticks() + 1000 
                                            for rect_info in memory_game_cases_selected:
                                                rect_info['clicked'] = False
                                        else:
                                            # On ajoute la paire aux cartes validées
                                            print(f'Mémo: tentative #{memory_game_click_count}: paire OK')
                                            memory_game_cases_found.extend(memory_game_cases_selected)

                elif state == TIC_TAC_TOE_STATE:
                    # On teste chaque case du tictactoe
                    for square_info in tictactoe_game_cases:
                        if square_info['square'].collidepoint(event.pos):
                            # Si ce n'est pas une case déjà cliquées
                            if not square_info['clicked'] and tictactoe_game_player_turn:
                                square_info['clicked'] = 'player'
                                tictactoe_game_player_turn = False
                                playerDelayDisplayUpdate = pygame.time.get_ticks() + 1000 

                elif state == QUIZ_STATE:
                    pass

    # On affiche les différents écran du jeux en fonction de l'état de "state"
    if state == START_STATE:
        display_start_screen()

    elif state == MENU_STATE:
        display_menu_screen()
        if lives == 0:
            display_score_barre(lives, False, "Fin de la partie", {"text": "Game Over!", "color": pygame.Color('red')})
        else:
            display_score_barre(lives)

    elif state == MEMORY_STATE:
        # Initilise le mémo s'il ne l'est pas déjà
        if not memory_game_cases and lives > 0:
            print("Mémo: initialisation")
            playerDelayDisplayUpdate = 0
            gameoverDelayDisplayUpdate = 0
            # Ré-initialise les résultats (dans le cas d'une nouvelle partie)
            memory_game_click_count = 0
            memory_game_cases_selected = []
            memory_game_cases_found = []

            memory_game_cases = initialize_memory_game()

        # quand le joueur a déja retourné 2 cartes et que le délai d'attente est atteint on réinitialise la liste des cartes cliquéés
        if len(memory_game_cases_selected) == 2 and playerDelayDisplayUpdate > 0 and pygame.time.get_ticks() >= playerDelayDisplayUpdate:
            memory_game_cases_selected.clear()

        display_score_barre(lives, True, "Nombre de tentatives: " + str(memory_game_click_count))

        display_memory_game(memory_game_cases, memory_game_cases_selected, memory_game_cases_found, memory_game_click_count)

        # FIN du mémo
        if memory_game_click_count >= MEMORY_GAME_MAX_TENTATIVES or len(memory_game_cases_found) == len(memory_game_cases):

            # On ajoute un délai (2s) en fin de partie pour avoir le temps de voir l'ensemble des cartes
            if gameoverDelayDisplayUpdate == 0:
                gameoverDelayDisplayUpdate = pygame.time.get_ticks() + 2000 

                # Si toutes les cartes ont été retournées
                if len(memory_game_cases_found) == len(memory_game_cases):
                    print(f'Mémo: gagné aprés {memory_game_click_count} tentatives')
                # Au delà de 10 tentatives on perd une vie
                elif memory_game_click_count >= MEMORY_GAME_MAX_TENTATIVES:
                    print(f'Mémo: perdu aprés {memory_game_click_count} tentatives')

            # Si toutes les cartes ont été retournées
            if len(memory_game_cases_found) == len(memory_game_cases):
                display_score_barre(lives, True,
                                    f"Nombre de tentatives: {memory_game_click_count}",
                                    {"text": "Well done !", "color": pygame.Color('green')})       

            # Au delà de 10 tentatives on perd une vie
            elif memory_game_click_count >= MEMORY_GAME_MAX_TENTATIVES:
                display_score_barre(lives, True,
                                    f"Nombre de tentatives: {memory_game_click_count}",
                                    {"text": "Perdu !", "color": pygame.Color('red')})

            if pygame.time.get_ticks() >= gameoverDelayDisplayUpdate:

                if len(memory_game_cases_found) < len(memory_game_cases):                  
                    # On décrémente le nombre de vies
                    if lives > 0:
                        lives -= 1
                        memory_game_cases_found.clear()
                        memory_game_cases_selected.clear()
                        # S'il reste au moins 1 vie au joueur on réinitialise le mémo
                        if lives >= 1:
                            memory_game_cases.clear()

                gameoverDelayDisplayUpdate = 0
                # On retourne au menu
                state = MENU_STATE

    elif state == TIC_TAC_TOE_STATE:
        # Initilise le tictactoe s'il ne l'est pas déjà
        if tictactoe_game_cases == [] and lives > 0:
            playerDelayDisplayUpdate = 0
            gameoverDelayDisplayUpdate = 0
            tictactoe_game_cases = initialize_tictactoe_game()
                    
            # Choisi aléatoirement qui commence la partie
            tictactoe_game_player_turn = random.choice([True,False])
            if tictactoe_game_player_turn:
                print(f"Tic Tac Toe: 'player' commence la partie")
            else:
                print(f"Tic Tac Toe: 'computer' commence la partie")       

        display_tictactoe_game(tictactoe_game_cases)

        # On regarde s'il y a un gagnant
        result, winner = check_tictactoe_game_over(tictactoe_game_cases)
        if result:
            # On ajoute un délai (2s) en fin de partie pour avoir le temps de voir le résultat
            if gameoverDelayDisplayUpdate == 0:
                print(f"Tic Tac Toe: le gagnant est {winner}")
                gameoverDelayDisplayUpdate = pygame.time.get_ticks() + 2000 

            if 'player' in winner:
                display_score_barre(lives, True,"fin de la partie: ",{"text": "Gagné !", "color": pygame.Color('green')})
            else:
                display_score_barre(lives, True,"fin de la partie: ",{"text": "Perdu !", "color": pygame.Color('red')})        

            if pygame.time.get_ticks() >= gameoverDelayDisplayUpdate:              
                # On décrémente le nombre de vies
                if lives > 0 and 'computer' in winner:
                    lives -= 1
                    # S'il reste au moins 1 vie au joueur on réinitialise le mémo
                    if lives >= 1:
                        tictactoe_game_cases.clear()

                gameoverDelayDisplayUpdate = 0
                # On retourne au menu
                state = MENU_STATE
        else:
            # Si c'est 'computer qui commence la partie on ajoute un délai (1s)
            if playerDelayDisplayUpdate == 0 and not tictactoe_game_player_turn and all(position['clicked'] is None for position in tictactoe_game_cases):
                playerDelayDisplayUpdate = pygame.time.get_ticks() + 1000 

            # Au tour de 'computer' de jouer
            if not tictactoe_game_player_turn and playerDelayDisplayUpdate > 0 and pygame.time.get_ticks() >= playerDelayDisplayUpdate:
                empty_square_case = random.choice([position for position in tictactoe_game_cases if not position['clicked']])
                empty_square_case['clicked'] = 'computer'
                tictactoe_game_player_turn = True

            display_score_barre(lives, True)

    elif state == QUIZ_STATE:
        run_quiz_game()
        display_score_barre(lives, True)

    elif state == END_STATE:
        display_final_screen()

    display_cursor()

    pygame.display.update()
    clock.tick(60)