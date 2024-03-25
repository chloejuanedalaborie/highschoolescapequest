#!/usr/bin/env python3

import pygame
import sys
import variables, outils, menu, memory, quiz, tictactoe

start_button_rect = pygame.Rect(252, 450, 100, 100)

def start_screen():
    # Affiche la page d'accueil du jeu
    fond = pygame.image.load("./images/title.png").convert()
    fond = pygame.transform.scale(fond, (variables.WINDOW_WIDTH, variables.WINDOW_HEIGHT))

    fenetre.blit(fond, (0, 0))
    fenetre.blit(play_button_image, play_button_rect)

def score_barre(bShowMenuButton=False, sScoreText="", dGameOverText={}):
    # Affiche la barre de score
    pygame.draw.rect(fenetre, WHITE, score_barre_rect, 0)
    score_text_font = pygame.font.Font(font_path, 12)
    gameover_font = pygame.font.Font(font_path, 48)

    life_text_surface = score_text_font.render("Vies :", True, GRAY)
    life_text_rect = life_text_surface.get_rect(topleft=(10, 10))
    fenetre.blit(life_text_surface, life_text_rect)
    for life_full in range(livesCount):
        fenetre.blit(life_full_image, (life_text_rect.width + 20 + (life_full * life_full_image.get_width()), 10))
    for life_empty in range(LIVES - livesCount):
        fenetre.blit(life_empty_image, (life_text_rect.width + 20 + (livesCount * (life_full_image.get_width())) + (life_empty * life_empty_image.get_width()), 10))

    score_text_surface = score_text_font.render(sScoreText, True, GRAY)
    score_text_rect = score_text_surface.get_rect(topleft=(10, 30))
    fenetre.blit(score_text_surface, score_text_rect)

    if dGameOverText:
        print(str(dGameOverText))
        complete_text_surface = gameover_font.render(dGameOverText['text'], True, dGameOverText['color'])
        complete_text_rect = complete_text_surface.get_rect(midleft=(score_text_rect.right + 20, 30)) # à décaler un peu à droite
        fenetre.blit(complete_text_surface, complete_text_rect)

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

    tictactoe_image_text_font = pygame.font.Font(font_path, 24)
    tictactoe_image_text_surface = tictactoe_image_text_font.render("Morpion", True, pygame.Color('black'))
    tictactoe_rect = pygame.draw.rect(fenetre, WHITE, tictactoe_button_rect, 2)
    tictactoe_image = pygame.transform.scale(tic_tac_toe_background, tictactoe_rect.size)
    tictactoe_image_text_rect = tictactoe_image_text_surface.get_rect(center=tictactoe_image.get_rect().center)
    tictactoe_image.blit(tictactoe_image_text_surface, tictactoe_image_text_rect)
    fenetre.blit(tictactoe_image, tictactoe_rect)

    quiz_image_text_font = pygame.font.Font(font_path, 24)
    quiz_image_text_surface = quiz_image_text_font.render("Quiz", True, pygame.Color('black'))
    quiz_rect = pygame.draw.rect(fenetre, WHITE, quiz_button_rect, 2)
    quiz_image = pygame.transform.scale(quiz_background, quiz_rect.size)
    quiz_image_text_rect = quiz_image_text_surface.get_rect(center=quiz_image.get_rect().center)
    quiz_image.blit(quiz_image_text_surface, quiz_image_text_rect)
    fenetre.blit(quiz_image, quiz_rect)

    # Afficher "Game Over !" quand le joeur n'a plus de vie
    if livesCount == 0:
        complete_text_surface = gameover_font.render("Game Over !", True, pygame.Color('red'))
        complete_text_rect = complete_text_surface.get_rect(center=(WINDOW_WIDTH // 2, 30))
        fenetre.blit(complete_text_surface, complete_text_rect)

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

def refresh_memory_game_cards_display():
    global memory_game_case
    global memory_game_results
    global memory_game_case_clicked

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

def memory_game():
    global memory_game_case_clicked
    global memory_game_click_count
    global memory_game_case
    global state
    global livesCount
    global final_memory_game_click_count

    MAX_TENTATIVES=2

    # Affiche le background du jeu mémo
    fenetre.blit(memory_background, (0, score_barre_rect.height))

    # Affiche la barre de score
    score_barre(True, "Nombre de tentatives: " + str(memory_game_click_count))

    init_memory_game()

    refresh_memory_game_cards_display()

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
                if livesCount >= 1:
                    memory_game_case.clear()

        # Si toutes les cartes ont été retournées, le jeu est fini on retourne au menu
        elif len(memory_game_results) == len(memory_game_case):
            gameover_color= pygame.Color('green')
            gameover_text = "Well done !"

        # Afficher "Perdu !" ou  "Well done !"
        print("Mémo gameover: " + gameover_text)
        score_barre(True, "Nombre de tentatives: " + str(memory_game_click_count), {"text": gameover_text, "color": gameover_color})

        # Afficher toutes les cases la couleur perdu ou gagné
        for rect_info in memory_game_case:
            rect_surf = pygame.Surface(rect_info['rectangle'].size)
            rect_surf.fill(gameover_color)
            fenetre.blit(rect_surf, rect_info['rectangle'])
            pygame.draw.rect(fenetre, WHITE, rect_info['rectangle'], 2)

        pygame.display.update()
        pygame.time.delay(2000)

        state = MENU_STATE

def init_tic_tac_toe_game():
    global tictactoe_game_case
    global livesCount
    global tictactoe_game_player_turn  
        
    # Initilise le tictactoe s'il ne l'est pas déjà
    if not tictactoe_game_case and livesCount > 0:
            
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
                tictactoe_game_case.append({'square': rect,'clicked': None})
                
        # Choisi aléatoirement qui commence la partie
        tictactoe_game_player_turn = random.choice([True,False])
    
def tic_tac_toe_game():
    global tictactoe_game_case
    global tictactoe_game_player_turn
    global state
    global livesCount

    init_tic_tac_toe_game()

    # Play the tic-tac-toe game
    fenetre.blit(tic_tac_toe_background, (0, score_barre_rect.height))

    if not tictactoe_game_player_turn:
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
        fenetre.blit(square_surf, square_info['square'])        

    # Affiche la barre de score
    score_barre(True)   

def quiz_game():
    # Play the quiz game
    fenetre.blit(quiz_background, (0, score_barre_rect.height))

    # Affiche la barre de score
    score_barre(True)

def gérer_curseur():
    # Display the cursor
    mouse_pos = pygame.mouse.get_pos()
    fenetre.blit(cursor_image, mouse_pos)

def memory_game_events(mousePosition):
    global menu_button_rect
    global memory_game_case
    global memory_game_results
    global state

    # Gestion du bouton de retour au menu
    if menu_button_rect.collidepoint(mousePosition):
        state = MENU_STATE

    # On teste chaque case du mémo
    for rect_info in memory_game_case:
        if rect_info['rectangle'].collidepoint(mousePosition):
            # Si ce n'est pas une case déjà cliquées ou validées, on l'ajoute à la liste des cases cliquées
            if not rect_info['clicked'] and rect_info not in memory_game_results:
                rect_info['clicked'] = True
                memory_game_case_clicked.append(rect_info)

def tictactoe_game_events(mousePosition):
    global menu_button_rect
    global tictactoe_game_case
    global tictactoe_game_player_turn
    global state

    # Gestion du bouton de retour au menu
    if menu_button_rect.collidepoint(mousePosition):
        state = MENU_STATE
        
    # On teste chaque case du tictactoe
    for square_info in tictactoe_game_case:
        if square_info['square'].collidepoint(mousePosition):
            # Si ce n'est pas une case déjà cliquées
            if not square_info['clicked']:
                square_info['clicked'] = 'player'
                tictactoe_game_player_turn = False

def quiz_game_events(mousePosition):
    global menu_button_rect
    global state

    # Gestion du bouton de retour au menu
    if menu_button_rect.collidepoint(mousePosition):
        state = MENU_STATE

def menu_events(mousePosition):
    global memo_button_rect
    global tictactoe_button_rect
    global quiz_button_rect
    global state

    if memo_button_rect.collidepoint(mousePosition):
       pygame.draw.rect(fenetre, LIGHT_BLUE, memo_button_rect, 2)
       state = MEMORY_STATE
    elif tictactoe_button_rect.collidepoint(mousePosition):
        pygame.draw.rect(fenetre, LIGHT_BLUE, tictactoe_button_rect, 2)
        state = TIC_TAC_TOE_STATE
    elif quiz_button_rect.collidepoint(mousePosition):
        pygame.draw.rect(fenetre, LIGHT_BLUE, quiz_button_rect, 2)
        state = QUIZ_STATE

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
            if variables.state == variables.START_STATE and start_button_rect.collidepoint(event.pos):
                    variables.state = variables.MENU_STATE
            # écran menu
            elif variables.state == variables.MENU_STATE:
                menu.events(event.pos)
            elif variables.state == variables.MEMORY_STATE:
                memory.events(event.pos)
            elif variables.state == variables.TIC_TAC_TOE_STATE:
                tictactoe.events(event.pos)
            elif variables.state == variables.QUIZ_STATE:
                quiz.events(event.pos)

def gestion_display():
        # On affiche les différents écran du jeux en fonction de l'état de "state"
        if variables.state == variables.START_STATE:
            start_screen()
        elif variables.state == variables.MENU_STATE:
            menu.screen()
        elif variables.state == variables.MEMORY_STATE:
            memory.screen()
        elif variables.state == variables.TIC_TAC_TOE_STATE:
            tictactoe.screen()
        elif variables.state == variables.QUIZ_STATE:
            quiz.screen()
        elif variables.state == variables.END_STATE:
            pass

if __name__ == "__main__":

    # Initialise PyGame
    pygame.init()
    clock = pygame.time.Clock()

    # Initialise le mixer pour la musique et les sons
    pygame.mixer.init()

    pygame.mixer.music.load('./musics/password-infinity-123276.mp3')
    pygame.mixer.music.play()

    # Création de la fenêtre
    fenetre = pygame.display.set_mode((variables.WINDOW_WIDTH, variables.WINDOW_HEIGHT))
    pygame.display.set_caption("High School Escape Quest")

    # Main game loop
    while True:
        gestion_events()

        gestion_display()

        outils.afficher_curseur()

        pygame.display.update()
        clock.tick(60)