import pygame
import sys
import random
import variables, outils

# Variables globales
tictactoe_game_case = []
delayDisplayUpdate = 0
finalDisplayUpdate = 0

def initialisation():
    global tictactoe_game_case
    global tictactoe_game_player_turn
    global delayDisplayUpdate
        
    # Initilise le tictactoe s'il ne l'est pas déjà
    if not tictactoe_game_case and variables.livesCount > 0:
        print("Mémo: initialisation")
        delayDisplayUpdate = 0

        # Dimensions des cases du tictactoe
        SQUARE_WIDTH = 105
        SQUARE_HEIGHT = 105
        GAP = 30  # Espace entre les rectangles

        # Calcul total de l'espace horizontal et vertical
        total_width = 3 * (SQUARE_WIDTH + GAP) - GAP
        total_height = 3 * (SQUARE_HEIGHT + GAP) - GAP

        # Position du coin supérieur gauche de la zone des rectangle
        start_x = ((variables.WINDOW_WIDTH - total_width) // 2) - (SQUARE_WIDTH // 4)
        start_y = ((variables.WINDOW_HEIGHT - variables.SCORE_BARRE_HEIGHT - total_height) // 2) + (SQUARE_HEIGHT // 4)

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
        if tictactoe_game_player_turn:
            print(f"Mémo: 'player' commence la partie")
        else:
            print(f"Mémo: 'computer' commence la partie")

def check_game_over():
    global tictactoe_game_case

    for i in range(3):
        # On test s'il y a une ligne compléte
        if tictactoe_game_case[i * 3]['clicked'] == tictactoe_game_case[i * 3 + 1]['clicked'] == tictactoe_game_case[i * 3 + 2]['clicked'] is not None:
            return True, tictactoe_game_case[i * 3]['clicked']
        # On test s'il y a une colonne compléte
        if tictactoe_game_case[i]['clicked'] == tictactoe_game_case[i + 3]['clicked'] == tictactoe_game_case[i + 6]['clicked'] is not None:
            return True, tictactoe_game_case[i]['clicked']

    # On test les 2 diagonales        
    if tictactoe_game_case[0]['clicked'] == tictactoe_game_case[4]['clicked'] == tictactoe_game_case[8]['clicked'] is not None:
        return True, tictactoe_game_case[0]['clicked']
    if tictactoe_game_case[2]['clicked'] == tictactoe_game_case[4]['clicked'] == tictactoe_game_case[6]['clicked'] is not None:
        return True, tictactoe_game_case[2]['clicked'] 

    return False, None

def screen():
    global tictactoe_game_case
    global tictactoe_game_player_turn
    global delayDisplayUpdate
    global finalDisplayUpdate

    # Play the tictactoe game
    fenetre_surface = pygame.display.get_surface()
    
    # Fond d'écran
    tictactoe_background = outils.image_surface("./images/salle_morpion.png", fenetre_surface.get_width(), fenetre_surface.get_height() - variables.SCORE_BARRE_HEIGHT)
    fenetre_surface.blit(tictactoe_background, (0, variables.SCORE_BARRE_HEIGHT))

    # Affiche la barre de score
    outils.score_barre(True)

    initialisation()

    text_font = pygame.font.Font(None, 92)
    
    for square_info in tictactoe_game_case:
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

    # On regarde s'il y a un gagnant
    result, winner = check_game_over()
    if result:
        # On ajoute un délai en fin de partie pour avoir le temps de voir le résultat
        if finalDisplayUpdate == 0:
            print(f"Tic Tac Toe: le gagnant est {winner}")
            finalDisplayUpdate = pygame.time.get_ticks() + 2000 

        if 'player' in winner:
            outils.score_barre(True,"fin de la partie: ",{"text": "Gagné !", "color": pygame.Color('green')})
        else:
            outils.score_barre(True,"fin de la partie: ",{"text": "Perdu !", "color": pygame.Color('red')})        

        if pygame.time.get_ticks() >= finalDisplayUpdate:              
            # On décrémente le nombre de vies
            if variables.livesCount > 0 and 'computer' in winner:
                variables.livesCount -= 1
                # S'il reste au moins 1 vie au joueur on réinitialise le mémo
                if variables.livesCount >= 1:
                    tictactoe_game_case.clear()

            finalDisplayUpdate = 0
            # On retourne au menu
            variables.state = variables.MENU_STATE
    else:
        # Si c'est 'computer qui commence la partie on ajoute un délai
        if delayDisplayUpdate == 0 and not tictactoe_game_player_turn and all(position['clicked'] is None for position in tictactoe_game_case):
            delayDisplayUpdate = pygame.time.get_ticks() + 1000 

        # Au tour de 'computer' de jouer
        if not tictactoe_game_player_turn and delayDisplayUpdate > 0 and pygame.time.get_ticks() >= delayDisplayUpdate:
            empty_square_case = random.choice([position for position in tictactoe_game_case if not position['clicked']])
            empty_square_case['clicked'] = 'computer'
            tictactoe_game_player_turn = True

def events(mousePosition):
    global menu_button_rect
    global tictactoe_game_case
    global tictactoe_game_player_turn
    global delayDisplayUpdate

    outils.score_barre_events(mousePosition)
        
    # On teste chaque case du tictactoe
    for square_info in tictactoe_game_case:
        if square_info['square'].collidepoint(mousePosition):
            # Si ce n'est pas une case déjà cliquées
            if not square_info['clicked'] and tictactoe_game_player_turn:
                square_info['clicked'] = 'player'
                tictactoe_game_player_turn = False
                delayDisplayUpdate = pygame.time.get_ticks() + 1000 

if __name__ == "__main__":
    # Initialise PyGame
    pygame.init()
    pygame.display.set_caption("tictactoe")
    pygame.mouse.set_visible(False) # cache le pointeur de la souris
    clock = pygame.time.Clock()

    # Création de la fenêtre
    fenetre = pygame.display.set_mode((variables.WINDOW_WIDTH, variables.WINDOW_HEIGHT))

    # Main game loop
    while True:

        for event in pygame.event.get():
            # Quitter le jeu
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Gestion du clic
            elif event.type == pygame.MOUSEBUTTONDOWN:        
                events(event.pos)

        screen()

        outils.afficher_curseur()

        pygame.display.update()
        clock.tick(60)