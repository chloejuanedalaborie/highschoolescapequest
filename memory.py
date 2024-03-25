import pygame
import sys
import random
import outils, variables

# Variables globales
memory_game_case = []
memory_game_case_clicked = []
memory_game_results = []
memory_game_click_count = 0
delayDisplayUpdate = 0
finalDisplayUpdate = 0
MAX_TENTATIVES = 10

def initialisation():
    global memory_game_case
    global memory_game_results
    global memory_game_click_count
    global delayDisplayUpdate

    # Initilise le mémo s'il ne l'est pas déjà
    if not memory_game_case and variables.livesCount > 0:
        print("Mémo: initialisation")
        memory_game_click_count = 0
        delayDisplayUpdate = 0

        # Dimensions des cases du mémo
        RECT_WIDTH = 105
        RECT_HEIGHT = 125
        GAP = 30  # Espace entre les rectangles

        # Calcul total de l'espace horizontal et vertical
        total_width = 4 * (RECT_WIDTH + GAP) - GAP
        total_height = 3 * (RECT_HEIGHT + GAP) - GAP

        # Position du coin supérieur gauche de la zone des rectangle
        start_x = ((variables.WINDOW_WIDTH - total_width) // 2) - (RECT_WIDTH // 4)
        start_y = ((variables.WINDOW_HEIGHT - variables.SCORE_BARRE_HEIGHT - total_height) // 2) + (RECT_HEIGHT // 4)

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

        # Ré-initialise les résultats (dans le cas d'une nouvelle partie)
        memory_game_results = []

def afficher_cartes():
    global memory_game_case
    global memory_game_results
    global memory_game_case_clicked
    global delayDisplayUpdate

    fenetre_surface = pygame.display.get_surface()

    # quand le joueur a déja retourné 2 cartes et que le délai d'attente est atteint on réinitialise la liste des cartes cliquéés
    if len(memory_game_case_clicked) == 2 and delayDisplayUpdate > 0 and pygame.time.get_ticks() >= delayDisplayUpdate:
        memory_game_case_clicked.clear()

    # On itére sur l'ensemble des cases
    for rect_info in memory_game_case:
        index = rect_info['image_index'] + 1
        rect_surf = outils.image_surface(f'./images/mémo/card_{index}.jpeg', 105, 125)
      
        # Si le joueur a perdu, on met toutes les cases en rouge
        if memory_game_click_count > MAX_TENTATIVES:
            rect_surf.fill(pygame.Color('red'))
        # Si le joueur a gagné, on met toutes les cases en vert
        elif len(memory_game_results) == len(memory_game_case):
            rect_surf.fill(pygame.Color('green'))
        # On affiche une case blanche si la case n'est pas déjà cliquées ou validées
        elif rect_info not in memory_game_results and rect_info not in memory_game_case_clicked:
            rect_surf.fill(pygame.Color('white'))

        fenetre_surface.blit(rect_surf, rect_info['rectangle'])

def screen():
    global memory_game_case_clicked
    global memory_game_click_count
    global memory_game_case
    global final_memory_game_click_count
    global finalDisplayUpdate

    # Play the memory game
    fenetre_surface = pygame.display.get_surface()
    
    # Fond d'écran
    memory_background = outils.image_surface("./images/salle_memo.png", fenetre_surface.get_width(), fenetre_surface.get_height() - variables.SCORE_BARRE_HEIGHT)
    fenetre_surface.blit(memory_background, (0, 50))

    # Affiche la barre de score
    outils.score_barre(True, "Nombre de tentatives: " + str(memory_game_click_count))

    initialisation()

    afficher_cartes()

    # FIN du mémo
    if memory_game_click_count >= MAX_TENTATIVES or len(memory_game_results) == len(memory_game_case):

        # On ajoute un délai en fin de partie pour avoir le temps de voir l'ensemble des cartes
        if finalDisplayUpdate == 0:
            finalDisplayUpdate = pygame.time.get_ticks() + 1000 

        if pygame.time.get_ticks() >= finalDisplayUpdate:

            # Si toutes les cartes ont été retournées, le jeu est fini on retourne au menu
            if len(memory_game_results) == len(memory_game_case):
                print(f'Mémo: gagné aprés {memory_game_click_count} tentatives')
                outils.score_barre(True,
                                   f"Nombre de tentatives: {memory_game_click_count}",
                                   {"text": "Well done !", "color": pygame.Color('green')})       

            # Au delà de 10 tentatives on perd une vie
            elif memory_game_click_count >= MAX_TENTATIVES:
                print(f'Mémo: perdu aprés {memory_game_click_count} tentatives')
                outils.score_barre(True,
                                   f"Nombre de tentatives: {memory_game_click_count}",
                                   {"text": "Perdu !", "color": pygame.Color('red')})
                
                # On décrémente le nombre de vies
                if variables.livesCount > 0:
                    variables.livesCount -= 1
                    memory_game_results.clear()
                    memory_game_case_clicked.clear()
                    # S'il reste au moins 1 vie au joueur on réinitialise le mémo
                    if variables.livesCount >= 1:
                        memory_game_case.clear()

            # On conserve le score final pour l'affichage sur le menu
            final_memory_game_click_count = memory_game_click_count
            finalDisplayUpdate = 0

            # On retourne au menu
            variables.state = variables.MENU_STATE

def events(mousePosition):
    global memory_game_case_clicked
    global memory_game_results
    global memory_game_click_count
    global delayDisplayUpdate

    outils.score_barre_events(mousePosition)

    if not memory_game_click_count >= MAX_TENTATIVES or not len(memory_game_results) == len(memory_game_case):
        # On teste chaque case du mémo
        for rect_info in memory_game_case:
            if rect_info['rectangle'].collidepoint(mousePosition):
                # Si ce n'est pas une case déjà cliquées ou validées, on l'ajoute à la liste des cases cliquées
                if not rect_info['clicked'] and rect_info not in memory_game_results and len(memory_game_case_clicked) < 2:
                    rect_info['clicked'] = True
                    memory_game_case_clicked.append(rect_info)

                    # On teste si une paire de carte a été retournée
                    if len(memory_game_case_clicked) == 2:
                        memory_game_click_count += 1
                        # Si la paire est incorrecte, on doit à nouveau cacher les cartes
                        if memory_game_case_clicked[0]['image_index'] != memory_game_case_clicked[1]['image_index']:
                            # On initialise un delai pour laisser au joueur le temps de voir la carte
                            print(f'Mémo: tentative #{memory_game_click_count}: paire KO')
                            delayDisplayUpdate = pygame.time.get_ticks() + 1000 
                            for rect_info in memory_game_case_clicked:
                                rect_info['clicked'] = False
                        else:
                            # On ajoute la paire aux cartes validées
                            print(f'Mémo: tentative #{memory_game_click_count}: paire OK')
                            memory_game_results.extend(memory_game_case_clicked)
                            # On réinitialise la liste des cartes cliquéés
                            memory_game_case_clicked.clear()

if __name__ == "__main__":
    # Initialise PyGame
    pygame.init()
    pygame.display.set_caption("memory")
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