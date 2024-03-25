import pygame
import sys
import random
import variables, outils

# Variables globales
tictactoe_game_case = []
tictactoe_game_case_clicked = []
tictactoe_game_result = []
tictactoe_game_click_count = 0
final_tictactoe_game_click_count = 0

def initialisation():
    global tictactoe_game_case
    global livesCount
    global tictactoe_game_player_turn  
        
    # Initilise le tictactoe s'il ne l'est pas déjà
    if not tictactoe_game_case and variables.livesCount > 0:
            
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

def screen():
    global tictactoe_game_case
    global tictactoe_game_player_turn
    global state
    global livesCount

    # Play the tictactoe game
    fenetre_surface = pygame.display.get_surface()
    
    # Fond d'écran
    tictactoe_background = outils.image_surface("./images/salle_morpion.png", fenetre_surface.get_width(), fenetre_surface.get_height() - variables.SCORE_BARRE_HEIGHT)
    fenetre_surface.blit(tictactoe_background, (0, variables.SCORE_BARRE_HEIGHT))

    # Affiche la barre de score
    outils.score_barre(True)

    initialisation()

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

def events(mousePosition):
    global menu_button_rect
    global tictactoe_game_case
    global tictactoe_game_player_turn

    outils.score_barre_events(mousePosition)
        
    # On teste chaque case du tictactoe
    for square_info in tictactoe_game_case:
        if square_info['square'].collidepoint(mousePosition):
            # Si ce n'est pas une case déjà cliquées
            if not square_info['clicked']:
                square_info['clicked'] = 'player'
                tictactoe_game_player_turn = False

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