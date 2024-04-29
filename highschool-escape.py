import pygame
import sys
import random
import json

# Variables pour maintenir l'état de la navigation dans le jeu
START_STATE = 'start'
LEVEL_STATE = 'level'
MENU_STATE = 'menu'
MEMORY_STATE = 'memory'
TIC_TAC_TOE_STATE = 'tic_tac_toe'
QUIZ_STATE = 'quiz'
END_STATE = 'game_over'

# Dimensions de la fenêtre
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

# Fonds d'écrans
TITLE_SCREEN_BACKGROUND_IMAGE = "./images/title.png"
MENU_BACKGROUND_IMAGE = "./images/plan_lycee.png"
MEMORY_BACKGROUND_IMAGE = "./images/salle_memo.png"
TICTACTOE_BACKGROUND_IMAGE = "./images/salle_morpion.png"
QUIZ_BACKGROUND_IMAGE = "./images/salle_quiz.png"

# Characters images
MEMORY_CHARACTER_IMAGE = "./images/memory-game-character.png"
TICTACTOE_CHARACTER_IMAGE = "./images/tic-tac-toe-game-character.png"
QUIZ_CHARACTER_IMAGE = "images/quiz-game-character.png"

# Musique et sons
GAME_MUSIC = "./musics/password-infinity-123276.mp3"
CLICK = "./musics/click.wav"
CORRECT = "./musics/correct.wav"
WRONG = "./musics/wrong.wav"
WIN = "./musics/game_win.wav"
LOST = "./musics/game_lost.wav"

# Zones de clics
MEMO_BUTTON_RECT = pygame.Rect(0, 50, 195, 255)
TICTACTOE_BUTTON_RECT = pygame.Rect(0, 309, 195, 292)
QUIZ_BUTTON_RECT = pygame.Rect(362, 248, 239, 353)
START_BUTTON_RECT = pygame.Rect(252, 475, 100, 100)
EASY_LEVEL_RECT = pygame.Rect(90, 199, 160, 31)
NORMAL_LEVEL_RECT = pygame.Rect(240, 199, 160, 31)
HARD_LEVEL_RECT = pygame.Rect(420, 199, 160, 31)

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

GAME_COMPLETED_IMAGE = "./images/Icon_Large_Star.png"

MAX_LIVES = 3
QUIZ_GAME_MAX_QUESTIONS = 10
QUIZ_GAME_WIN_LIMIT = 8

def display_start_screen(scenario):
    """
    Affiche l'écran de départ puis après 1500 millisecondes,
    affiche un scénario chargé aléatoirement

    Args:
        scenario (dict): scénario chargé aléatoirement tiré d'un fichier json

    Return:
        None
    """
    fenetre_surface = pygame.display.get_surface()

    # Affiche la page d'accueil du jeu
    title_background = pygame.image.load(TITLE_SCREEN_BACKGROUND_IMAGE).convert()
    title_background = pygame.transform.scale(title_background, (WINDOW_WIDTH, WINDOW_HEIGHT))

    fenetre_surface.blit(title_background, (0, 0))

    # Blitter le bouton sur l'écran
    if playerDelayDisplayUpdate > 0 and pygame.time.get_ticks() >= playerDelayDisplayUpdate:
        # Création d'un rectangle translucide pour accueillir les différents scénarios
        title_rect_width = fenetre_surface.get_width() * 0.8
        title_rect_height = fenetre_surface.get_rect().height * 0.5
        title_rect_x = (fenetre_surface.get_width() * 0.2)//2
        title_rect_y = (fenetre_surface.get_rect().height * 0.5)//2
        title_rect = pygame.Rect(title_rect_x, title_rect_y, title_rect_width, title_rect_height)
        title_surf = pygame.Surface((title_rect.width, title_rect.height))
        title_surf.fill(pygame.Color('white'))
        title_surf.set_alpha(200)
        fenetre_surface.blit(title_surf, title_rect)

        afficher_texte_avec_retour_a_la_ligne(fenetre_surface,
                                              title_rect,
                                              pygame.Color('black'),
                                              pygame.font.Font(GAME_FONTS, 16),
                                              scenario['introduction'])

        # Charger l'image du bouton
        start_button_image = pygame.image.load('./images/bouton_play.png').convert_alpha()
        start_button_image = pygame.transform.scale(start_button_image, (START_BUTTON_RECT.width, START_BUTTON_RECT.height))
        fenetre_surface.blit(start_button_image, START_BUTTON_RECT)


def display_level_screen():
    """
    Affiche l'écran de sélection du niveau de difficulté

    Return:
        None
    """
    fenetre_surface = pygame.display.get_surface()

    # Affiche la page d'accueil du jeu
    title_background = pygame.image.load(TITLE_SCREEN_BACKGROUND_IMAGE).convert()
    title_background = pygame.transform.scale(title_background, (WINDOW_WIDTH, WINDOW_HEIGHT))

    fenetre_surface.blit(title_background, (0, 0))

    # Création d'un rectangle translucide pour accueillir les différents scénarios
    level_rect_width = fenetre_surface.get_width() * 0.8
    level_rect_height = fenetre_surface.get_rect().height * 0.7
    level_rect_x = (fenetre_surface.get_width() * 0.2)//2
    level_rect_y = (fenetre_surface.get_rect().height * 0.5)//2
    level_rect = pygame.Rect(level_rect_x, level_rect_y, level_rect_width, level_rect_height)
    level_surf = pygame.Surface((level_rect.width, level_rect.height))
    level_surf.fill(pygame.Color('white'))
    level_surf.set_alpha(200)
    fenetre_surface.blit(level_surf, level_rect)

    level_select_font = pygame.font.Font(GAME_FONTS, 30)
    level_select_font.set_italic(True)
    level_select_text_surf = level_select_font.render("Level Select", True, pygame.Color('red'))
    if show_text:
        fenetre_surface.blit(level_select_text_surf, level_select_text_surf.get_rect(midtop=(fenetre_surface.get_rect().centerx,level_rect.top + 10)))

    level_font = pygame.font.Font(GAME_FONTS, 24)
    level_font.set_italic(True)

    level_text_rect = pygame.Rect(level_rect.left + 10, 300, level_rect_width - 20, level_rect_height - (level_select_font.get_height() + level_font.get_height()) - 20)

    # si le pointeur de la souris est au-dessus du text on colorie en bleu
    if EASY_LEVEL_RECT.collidepoint(pygame.mouse.get_pos()):
        easy_text_surf = level_select_font.render("Easy", True, pygame.Color('blue'))
        easy_message = """
        Bienvenue dans le niveau Facile ! C'est comme une journée sans devoirs, une équation simple à résoudre, ou un épisode de votre série préférée.
        C'est relaxant, amusant et sans pression. Mais n'oubliez pas, chaque grand défi commence par une première étape facile. Alors, êtes-vous prêt à vous lancer dans l'aventure ?
        """
        afficher_texte_avec_retour_a_la_ligne(fenetre_surface,
                                              level_text_rect,
                                              pygame.Color('black'),
                                              pygame.font.Font(GAME_FONTS, 16),
                                              easy_message)
    else:
        easy_text_surf = level_select_font.render("Easy", True, pygame.Color('black'))
    fenetre_surface.blit(easy_text_surf, EASY_LEVEL_RECT)

    # si le pointeur de la souris est au-dessus du text on colorie en bleu
    if NORMAL_LEVEL_RECT.collidepoint(pygame.mouse.get_pos()):
        normal_text_surf = level_select_font.render("Normal", True, pygame.Color('blue'))
        normal_message = """
        Voici le niveau Normal, l'équilibre parfait entre le défi et l'amusement. C'est comme résoudre un problème de maths un peu corsé ou apprendre une nouvelle langue.
        Vous savez, ce sentiment quand vous résolvez un problème après y avoir longuement réfléchi ? C'est exactement ce qui vous attend ici.
        Prêt à mettre votre cerveau en action et à vous amuser en même temps ?
        """
        afficher_texte_avec_retour_a_la_ligne(fenetre_surface,
                                              level_text_rect,
                                              pygame.Color('black'),
                                              pygame.font.Font(GAME_FONTS, 16),
                                              normal_message)
    else:
        normal_text_surf = level_select_font.render("Normal", True, pygame.Color('black'))
    fenetre_surface.blit(normal_text_surf, NORMAL_LEVEL_RECT)

    # si le pointeur de la souris est au-dessus du text on colorie en bleu
    if HARD_LEVEL_RECT.collidepoint(pygame.mouse.get_pos()):
        hard_text_surf = level_select_font.render("Hard", True, pygame.Color('blue'))
        hard_message = """
        Bienvenue au niveau Difficile, le sommet de la montagne, le boss final. C'est ici que les vrais gamers brillent et que les légendes sont écrites.
        Vous vous sentirez peut-être comme un poisson hors de l'eau, mais rappelez-vous, chaque grand défi offre une grande récompense.
        Alors, préparez-vous, mettez votre casquette de gamer et voyons si vous êtes à la hauteur !
        """
        afficher_texte_avec_retour_a_la_ligne(fenetre_surface,
                                              level_text_rect,
                                              pygame.Color('black'),
                                              pygame.font.Font(GAME_FONTS, 16),
                                              hard_message)
    else:
        hard_text_surf = level_select_font.render("Hard", True, pygame.Color('black'))
    fenetre_surface.blit(hard_text_surf, HARD_LEVEL_RECT)


def display_menu_screen():
    """
    Affiche le menu une fois le bouton play de start_screen appuyé
    puis créé des zones cliquables sur chaque zones de jeu qui permettent d'accéder au jeu

    Return:
        None
    """
    fenetre_surface = pygame.display.get_surface()

    # Fond d'écran
    menu_background = pygame.image.load(MENU_BACKGROUND_IMAGE).convert()
    menu_background = pygame.transform.scale(menu_background, (fenetre_surface.get_width(), fenetre_surface.get_height()))
    fenetre_surface.blit(menu_background, (0, 0))

    # Création de la surface grise où apparaitront les jeux gagnés
    completed_game_rect = pygame.Rect(456,51,144,192)
    completed_game_surf = pygame.Surface((completed_game_rect.width, completed_game_rect.height))
    completed_game_surf.fill(pygame.Color('gray'))
    game_surf_height = completed_game_surf.get_height()//3

    game_completed_image = pygame.image.load(GAME_COMPLETED_IMAGE).convert_alpha()
    game_completed_image = pygame.transform.scale(game_completed_image, (25, 25))

    # Si aucun jeu n'a été gagné on affiche la case "locked"
    if not memory_game_completed and not quiz_game_completed and not tictactoe_game_completed:
        locked_font = pygame.font.Font(GAME_FONTS, 24)
        locked_surface = locked_font.render("Locked", True, pygame.Color('black'))
        locked_rect = locked_surface.get_rect(center=completed_game_surf.get_rect().center)
        completed_game_surf.blit(locked_surface, locked_rect)
    else:
        # Si le jeu Mémo est complété alors il apparait avec l'étoile dans le rectangle
        if memory_game_completed:
            memory_game_completed_font = pygame.font.Font(GAME_FONTS, 18)
            memory_game_completed_surface = memory_game_completed_font.render("Mémo", True, pygame.Color('gray44'))
            memory_game_completed_rect = memory_game_completed_surface.get_rect(topleft=(40, completed_game_surf.get_rect().top + 20))
            completed_game_surf.blit(game_completed_image, (memory_game_completed_rect.left - 30,memory_game_completed_rect.top - 5))
            completed_game_surf.blit(memory_game_completed_surface, memory_game_completed_rect)

        # Si le jeu Morpion est complété alors il apparait avec l'étoile dans le rectangle
        if tictactoe_game_completed:
            tictactoe_game_completed_font = pygame.font.Font(GAME_FONTS, 18)
            tictactoe_game_completed_surface = tictactoe_game_completed_font.render("Morpion", True, pygame.Color('gray44'))
            tictactoe_game_completed_rect = tictactoe_game_completed_surface.get_rect(topleft=(40 ,completed_game_surf.get_rect().top + game_surf_height + 20))
            completed_game_surf.blit(game_completed_image, (tictactoe_game_completed_rect.left - 30,tictactoe_game_completed_rect.top - 5))
            completed_game_surf.blit(tictactoe_game_completed_surface, tictactoe_game_completed_rect)

        # Si le jeu Quiz est complété alors il apparait avec l'étoile dans le rectangle
        if quiz_game_completed:
            quiz_game_completed_font = pygame.font.Font(GAME_FONTS, 18)
            quiz_game_completed_surface = quiz_game_completed_font.render("Quiz", True, pygame.Color('gray44'))
            quiz_game_completed_rect = quiz_game_completed_surface.get_rect(topleft=(40, completed_game_surf.get_rect().top + 2*game_surf_height + 20))
            completed_game_surf.blit(game_completed_image, (quiz_game_completed_rect.left - 30,quiz_game_completed_rect.top - 5))
            completed_game_surf.blit(quiz_game_completed_surface, quiz_game_completed_rect)

    fenetre_surface.blit(completed_game_surf, completed_game_rect)

    # si le pointeur de la souris est au-dessus de la zone on charge l'image du Character
    if MEMO_BUTTON_RECT.collidepoint(pygame.mouse.get_pos()) or memory_game_completed:
        # Charger l'image du bouton
        button_image = pygame.image.load(MEMORY_CHARACTER_IMAGE).convert()
        # Mettre à l'échelle l'image pour qu'elle s'adapte à la taille du bouton
        button_image = pygame.transform.scale(button_image, MEMO_BUTTON_RECT.size)
    else:
        # Charger l'image du bouton
        button_image = pygame.image.load(MEMORY_BACKGROUND_IMAGE).convert()
        # Mettre à l'échelle l'image pour qu'elle s'adapte à la taille du bouton
        button_image = pygame.transform.scale(button_image, MEMO_BUTTON_RECT.size)

        # Ajouter du texte au bouton
        text_font = pygame.font.Font(GAME_FONTS, 24)
        text_surface = text_font.render("Mémo", True, pygame.Color('black'))
        text_rect = text_surface.get_rect(center=button_image.get_rect().center)
        button_image.blit(text_surface, text_rect.topleft)

    # Blitter le bouton sur l'écran
    fenetre_surface.blit(button_image, MEMO_BUTTON_RECT)

    # si le pointeur de la souris est au-dessus de la zone on charge l'image du Character
    if TICTACTOE_BUTTON_RECT.collidepoint(pygame.mouse.get_pos()) or tictactoe_game_completed:
        # Charger l'image du bouton
        button_image = pygame.image.load(TICTACTOE_CHARACTER_IMAGE).convert()
        # Mettre à l'échelle l'image pour qu'elle s'adapte à la taille du bouton
        button_image = pygame.transform.scale(button_image, TICTACTOE_BUTTON_RECT.size)
    else:
        # Charger l'image du bouton
        button_image = pygame.image.load(TICTACTOE_BACKGROUND_IMAGE).convert()
        # Mettre à l'échelle l'image pour qu'elle s'adapte à la taille du bouton
        button_image = pygame.transform.scale(button_image, TICTACTOE_BUTTON_RECT.size)

        # Ajouter du texte au bouton
        text_font = pygame.font.Font(GAME_FONTS, 24)
        text_surface = text_font.render("Morpion", True, pygame.Color('black'))
        text_rect = text_surface.get_rect(center=button_image.get_rect().center)
        button_image.blit(text_surface, text_rect.topleft)

    # Blitter le bouton sur l'écran
    fenetre_surface.blit(button_image, TICTACTOE_BUTTON_RECT)

    # si le pointeur de la souris est au-dessus de la zone on charge l'image du Character
    if QUIZ_BUTTON_RECT.collidepoint(pygame.mouse.get_pos()) or quiz_game_completed:
        # Charger l'image du bouton
        button_image = pygame.image.load(QUIZ_CHARACTER_IMAGE).convert()
        # Mettre à l'échelle l'image pour qu'elle s'adapte à la taille du bouton
        button_image = pygame.transform.scale(button_image, QUIZ_BUTTON_RECT.size)
    else:
        # Charger l'image du bouton
        button_image = pygame.image.load(QUIZ_BACKGROUND_IMAGE).convert()
        # Mettre à l'échelle l'image pour qu'elle s'adapte à la taille du bouton
        button_image = pygame.transform.scale(button_image, QUIZ_BUTTON_RECT.size)

        # Ajouter du texte au bouton
        text_font = pygame.font.Font(GAME_FONTS, 24)
        text_surface = text_font.render("Quiz", True, pygame.Color('black'))
        text_rect = text_surface.get_rect(center=button_image.get_rect().center)
        button_image.blit(text_surface, text_rect.topleft)

    # Blitter le bouton sur l'écran
    fenetre_surface.blit(button_image, QUIZ_BUTTON_RECT)

def display_score_barre(lives, bShowMenuButton=False, sScoreText="", dGameOverText={}):
    """
    Affiche la barre de score du jeu.

    Args:
        lives (int): nombres de points de vie
        bShowMenuButton (bool, optional): Montre ou non le bouton guidant au menu, False par défaut
        sScoreText (str, optional): affiche le score."" par défaut.
        dGameOverText (dict, optional): Un dictionnaire contenant le texte et la couleur à afficher
        en fin de partie. Par défaut, {}.
    Returns:
        None
    """

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
    """
    Permet d'initialiser le jeux du memory.
    Mélange les carte et charge l'interface du memory.

    Returns:
        List:   Liste de dictionnaires représentant les cartes du jeu.
                Chaque dictionnaire contient un rectangle pygame et l'index
                de l'image associée
    """

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
    index_images_disponibles = random.sample(list(range(1,7)) * 2, k=len(rect_positions))

    # Combine (zip) les index d'images et les cases du jeu
    return [{'rectangle': pygame.Rect(position[0], position[1], RECT_WIDTH, RECT_HEIGHT), 'image_index': image_index}
            for position, image_index in zip(rect_positions, index_images_disponibles)]

def display_memory_game(cases, cases_selected, cases_found, memory_game_click_count):
    """
    (description)

    Args:
        cases (List):   Liste de dictionnaires représentant les cartes du jeu.
                        Chaque dictionnaire contient un rectangle pygame et l'index
                        de l'image associée.
        cases_selected (List): Liste des cases sélectionnées/retournées par le joueur
        cases_found (List): Liste des paires de cartes déjà trouvées par le joueur
        memory_game_click_count (int): Nombre de clics du joueur sur les cases dans la partie

    Returns:
        None
    """

    # Obtiens la surface de la fenêztre actuelle
    fenetre_surface = pygame.display.get_surface()

    # Fond d'écran
    memory_background = pygame.image.load(MEMORY_BACKGROUND_IMAGE).convert()
    memory_background = pygame.transform.scale(memory_background, (fenetre_surface.get_width(), fenetre_surface.get_height() - SCORE_BARRE_HEIGHT))
    fenetre_surface.blit(memory_background, (0, SCORE_BARRE_HEIGHT))

    # On itére sur l'ensemble des cases
    for rect_info in cases:
        rect_surf=pygame.Surface(rect_info['rectangle'].size)
        # Si le joueur a gagné, on met toutes les cases en vert
        if len(cases_found) == len(cases):
            rect_surf.fill(pygame.Color('green'))
        # Si le joueur a perdu, on met toutes les cases en rouge
        elif memory_game_click_count >= MEMORY_GAME_MAX_TENTATIVES:
            rect_surf.fill(pygame.Color('red'))
        # On affiche une case blanche si la case n'est pas déjà cliquées ou validées
        elif rect_info not in cases_found and rect_info not in cases_selected:
            rect_surf.fill(pygame.Color('white'))
        # Sinon on affiche l'image
        else:
            index = rect_info['image_index']
            rect_surf = pygame.image.load(f'./images/mémo/card_{index}.jpeg').convert()
            rect_surf = pygame.transform.scale(rect_surf, (105, 125))

        fenetre_surface.blit(rect_surf, rect_info['rectangle'])

def initialize_tictactoe_game():
    """
    Permet d'initialiser le jeu du tic tac toe en affichant les cases du jeu

    Returns:
        List:   Liste de dictionnaires représentant les cases du jeu.
                Chaque dictionnaire contient un rectangle pygame et
                un état 'clicked' initialisé à None.
    """

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
    """
    Permet de vérifier s'il y a un vainqueur
    (et donc si c'est la fin de la partie)

    Arguments:
        cases (List):   Liste de  dictionnaires représentant les  cases du morpion.
                        Chaque dictionnaire devrait avoir une clé 'clicked'
                        pour indiquer si la case a été sélectionnée ou non.

    Returns:
        String: 'player' ou 'computer' ou 'égalité'
        None: s'il n'y a pas de vainqueur
    """
    for i in range(3):
        # On teste s'il y a une ligne compléte
        if cases[i * 3]['clicked'] == cases[i * 3 + 1]['clicked'] == cases[i * 3 + 2]['clicked'] is not None:
            return cases[i * 3]['clicked']
        # On teste s'il y a une colonne compléte
        if cases[i]['clicked'] == cases[i + 3]['clicked'] == cases[i + 6]['clicked'] is not None:
            return cases[i]['clicked']

    # On teste les 2 diagonales
    if cases[0]['clicked'] == cases[4]['clicked'] == cases[8]['clicked'] is not None:
        return cases[0]['clicked']
    if cases[2]['clicked'] == cases[4]['clicked'] == cases[6]['clicked'] is not None:
        return cases[2]['clicked']

    # On enfin teste si toutes les cases ont été cliquées
    if None not in [case['clicked'] for case in cases]:
        return "égalité"
    else:
        return None

def display_tictactoe_game(cases):
    """
    Affiche l'état actuel du jeu de morpion Tic Tac Toe.

    Args:
        cases (List):   Une liste de dictionnaires représentant les cases du jeu.
                        Chaque dictionnaire contient un rectangle pygame et
                        l'état 'clicked' indiquant si la case a été sélectionnée (et par qui).
    """

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

def afficher_texte_avec_retour_a_la_ligne(surface, rect, couleur, font, texte):
    """
    Affiche le texte avec retour à la ligne dans la surface donnée.

    Args:
        surface (pygame.Surface): La surface sur laquelle afficher le texte.
        rect (pygame.Rect): Le rectangle définissant la position et la taille de la zone d'affichage.
        couleur (tuple): La couleur du texte (par exemple, (255, 255, 255) pour blanc).
        font (pygame.font.Font): L'objet de police à utiliser pour le texte.
        texte (str): Le texte à afficher.

    Returns:
        None
    """
    mots = texte.split()
    lignes = []
    ligne_actuelle = ""
    for mot in mots:
        test_ligne = ligne_actuelle + mot + " "
        if font.size(test_ligne)[0] < rect.width - 20:
            ligne_actuelle = test_ligne
        else:
            lignes.append(ligne_actuelle)
            ligne_actuelle = mot + " "
    lignes.append(ligne_actuelle)

    y_offset = 0
    for ligne in lignes:
        surface_ligne = font.render(ligne, True, couleur)
        rect_ligne = surface_ligne.get_rect(left=rect.left + 10, top=rect.top + 10 + y_offset)
        surface.blit(surface_ligne, rect_ligne)
        y_offset += font.get_height()

def initialize_quiz_game():
    """
    Permet d'initialiser le jeu quiz en chargeant les questions avec leur réponses

    Returns:
        quiz_question(List): liste des questions-réponses avec leur placement et position
    """
    print("Quiz: initialisation")

    with open('./quiz-questions-list.json', encoding='utf-8') as f:
        quiz_questions_all = json.load(f)

    quiz = [question for question in quiz_questions_all if question['difficulty'] == game_level]

    # on randomize la liste et on réduit le nombre de question à MAX_QUIZ_QUESTIONS
    quiz = random.sample(quiz, k=QUIZ_GAME_MAX_QUESTIONS)

    item_x = (fenetre_surface.get_width() * 0.2)//2 + 10
    quiz_question_rect_y = ((fenetre_surface.get_height() - SCORE_BARRE_HEIGHT) * 0.2)//2 + SCORE_BARRE_HEIGHT + 10

    question_rect_width = (fenetre_surface.get_width() * 0.8) - 20
    answer_rect_width = question_rect_width - 100
    answer_rect_height = (((fenetre_surface.get_height() - SCORE_BARRE_HEIGHT) * 0.8) - 40) // 6
    question_rect_heigth = answer_rect_height * 2

    quiz_questions = []
    for idx, question in enumerate(quiz):
        quiz_questions.append({
            'question': {
                'rect': pygame.Rect(item_x, quiz_question_rect_y, question_rect_width, question_rect_heigth),
                'text': f"{QUIZ_GAME_MAX_QUESTIONS - idx}: {question['question']}"
            },
            'answers': []
        })
        first_answer_rect_top = quiz_question_rect_y + 10 + question_rect_heigth + 5

        # on mélange également la liste de réponse
        for index, answer in enumerate(random.sample(question['answers'], k=len(question['answers']))):
            top = first_answer_rect_top + (answer_rect_height + 5) * index

            quiz_questions[-1]['answers'].append({
                # on decale le rect pour le text de 100 pour laisser la place à une image
                'rect': pygame.Rect(item_x + 100, top, answer_rect_width, answer_rect_height),
                'text': answer['answer'],
                'isCorrect': answer['isCorrect']
            })

    return quiz_questions

def display_quiz_game(item):
    """
    Créé le rectangle on apparaissent les questions/réponses du quiz et
    affiche une question ; si la réponses cliquée est correcte elle apparait en vert
    sinon en rouge

    Args:
        item (List): liste de questions-réponses avec leur placement et position

    Return:
        None
    """
    fenetre_surface = pygame.display.get_surface()

    # Fond d'écran
    quiz_background = pygame.image.load(QUIZ_BACKGROUND_IMAGE).convert()
    quiz_background = pygame.transform.scale(quiz_background, (fenetre_surface.get_width(), fenetre_surface.get_height() - SCORE_BARRE_HEIGHT))
    fenetre_surface.blit(quiz_background, (0, SCORE_BARRE_HEIGHT))

    # Création d'un rectangle translucide pour accueillir la question et les réponses
    quiz_question_rect_width = fenetre_surface.get_width() * 0.8
    quiz_question_rect_x = (fenetre_surface.get_width() * 0.2)//2
    quiz_question_rect_height = (fenetre_surface.get_rect().height - SCORE_BARRE_HEIGHT) * 0.8
    quiz_question_rect_y = ((fenetre_surface.get_rect().height - SCORE_BARRE_HEIGHT) * 0.2)//2 + SCORE_BARRE_HEIGHT
    quiz_question_rect = pygame.Rect(quiz_question_rect_x, quiz_question_rect_y, quiz_question_rect_width, quiz_question_rect_height)
    quiz_question_surf = pygame.Surface((quiz_question_rect.width, quiz_question_rect.height))
    quiz_question_surf.fill(pygame.Color('white'))
    quiz_question_surf.set_alpha(200)
    fenetre_surface.blit(quiz_question_surf, quiz_question_rect)

    # Affichage de la question
    afficher_texte_avec_retour_a_la_ligne(fenetre_surface,
                                          item['question']['rect'],
                                          pygame.Color('black'),
                                          pygame.font.Font(GAME_FONTS, 18),
                                          item['question']['text'])

    # Affichage des réponses
    for index, item2 in enumerate(item[('answers')]):
        quiz_answer_bullet_img = pygame.image.load(f"./images/quiz{index}.png").convert_alpha()
        quiz_answer_bullet_img = pygame.transform.scale(quiz_answer_bullet_img, (30, 30))
        fenetre_surface.blit(quiz_answer_bullet_img, (item['question']['rect'].left + 50, item2['rect'].top + 5))

        # Si le joueur a déjà répondu on affiche en vert la bonne réponse, en rouge les mauvaises
        if playerDelayDisplayUpdate > 0:
            if item2['isCorrect']:
                afficher_texte_avec_retour_a_la_ligne(fenetre_surface,
                                            item2['rect'],
                                            pygame.Color('forestgreen'),
                                            pygame.font.Font(GAME_FONTS, 18),
                                            item2['text'])
            else:
                afficher_texte_avec_retour_a_la_ligne(fenetre_surface,
                                            item2['rect'],
                                            pygame.Color('red'),
                                            pygame.font.Font(GAME_FONTS, 18),
                                            item2['text'])
        elif item2['rect'].collidepoint(pygame.mouse.get_pos()):
            afficher_texte_avec_retour_a_la_ligne(fenetre_surface,
                                        item2['rect'],
                                        pygame.Color('black'),
                                        pygame.font.Font(GAME_FONTS, 18),
                                        item2['text'])
        else:
            afficher_texte_avec_retour_a_la_ligne(fenetre_surface,
                                        item2['rect'],
                                        pygame.Color('gray50'),
                                        pygame.font.Font(GAME_FONTS, 18),
                                        item2['text'])

def display_final_screen(text):
    """
    Lorsque le jeu est fini (tous les jeux complétés ou plus de vie)
    on affiche l'image du jeu avec un rectangle translucide
    on y affiche alors le texte correspondant (conclusionWin ou clonclusionLose)

    Args:
        text (List): texte de la conclusion appropriée (conclusionWin ou clonclusionLose)

    Return:
        None
    """
    fenetre_surface = pygame.display.get_surface()

    # On réutilise la page d'accueil du jeu
    final_screen_background = pygame.image.load(TITLE_SCREEN_BACKGROUND_IMAGE).convert()
    final_screen_background = pygame.transform.scale(final_screen_background, (WINDOW_WIDTH, WINDOW_HEIGHT))

    fenetre_surface.blit(final_screen_background, (0, 0))

    # Création d'un rectangle translucide pour accueillir les différents scénarios de fin
    final_screen_rect_width = fenetre_surface.get_width() * 0.8
    final_screen_rect_height = fenetre_surface.get_rect().height * 0.5
    final_screen_rect_x = (fenetre_surface.get_width() * 0.2)//2
    final_screen_rect_y = (fenetre_surface.get_rect().height * 0.5)//2
    final_screen_rect = pygame.Rect(final_screen_rect_x, final_screen_rect_y, final_screen_rect_width, final_screen_rect_height)
    final_screen_surf = pygame.Surface((final_screen_rect.width, final_screen_rect.height))
    final_screen_surf.fill(pygame.Color('white'))
    final_screen_surf.set_alpha(200)
    fenetre_surface.blit(final_screen_surf, final_screen_rect)

    afficher_texte_avec_retour_a_la_ligne(fenetre_surface,
                                          final_screen_rect,
                                          pygame.Color('black'),
                                          pygame.font.Font(GAME_FONTS, 16),
                                          text)

# Remplace le curseur de la souris par une image
def display_cursor():
    """
    Cache le pointeur de souris et le remplace par un custom

    Returns:
        None
    """
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

pygame.mixer.music.load(GAME_MUSIC)
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

sound_click = pygame.mixer.Sound(CLICK)
sound_correct = pygame.mixer.Sound(CORRECT)
sound_wrong = pygame.mixer.Sound(WRONG)
sound_win = pygame.mixer.Sound(WIN)
sound_lost = pygame.mixer.Sound(LOST)

with open('./game-scenario-list.json', encoding='utf-8') as f:
    game_scenarios = json.load(f)

# selection d'un scénario aléatoirement
game_scenario = random.choice(game_scenarios)


# Création de la fenêtre
pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(f"High School Escape Quest: {game_scenario['scenario']}")

state = START_STATE
lives = MAX_LIVES
score = 0

# Variables pour permettre d'ajouter du délai à l'affichage
playerDelayDisplayUpdate = pygame.time.get_ticks() + 1500
gameoverDelayDisplayUpdate = 0

# Variables Tic Tac Toe
tictactoe_game_cases = []
tictactoe_game_player_turn = None
tictactoe_game_completed = False

# Variables Mémo
memory_game_cases = []
memory_game_cases_selected = []
memory_game_cases_found = []
memory_game_click_count = 0
memory_game_completed = False

# Variables Quiz
quiz_game_questions = []
quiz_game_current_question = None
quiz_game_score = 0
quiz_game_completed = False

game_over = False

font_fade = pygame.USEREVENT + 1
pygame.time.set_timer(font_fade, 250)
show_text = True

# Boucle principale du jeu
while True:
    fenetre_surface = pygame.display.get_surface()

    for event in pygame.event.get():
        # Quitter le jeu
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == font_fade:
            show_text = not show_text

        # Gestion du clic
        elif event.type == pygame.MOUSEBUTTONDOWN:

            # écran d'accueil
            if state == START_STATE:
                if playerDelayDisplayUpdate > 0 and pygame.time.get_ticks() >= playerDelayDisplayUpdate:
                    if START_BUTTON_RECT.collidepoint(event.pos):
                        sound_click.play()
                        state = LEVEL_STATE

            # écran choix niveau de difficulté
            elif state == LEVEL_STATE:
                if EASY_LEVEL_RECT.collidepoint(event.pos):
                    print('Level: le joueur a choisi le niveau "Easy"')
                    game_level = "easy"
                    MEMORY_GAME_MAX_TENTATIVES = 12
                    sound_click.play()
                    state = MENU_STATE
                if NORMAL_LEVEL_RECT.collidepoint(event.pos):
                    print('Level: le joueur a choisi le niveau "Normal"')
                    game_level = "medium"
                    MEMORY_GAME_MAX_TENTATIVES = 10
                    sound_click.play()
                    state = MENU_STATE
                if HARD_LEVEL_RECT.collidepoint(event.pos):
                    print('Level: le joueur a choisi le niveau "Hard"')
                    game_level = "hard"
                    MEMORY_GAME_MAX_TENTATIVES = 9
                    sound_click.play()
                    state = MENU_STATE

            # écran menu
            elif state == MENU_STATE:
                if MEMO_BUTTON_RECT.collidepoint(event.pos) and not memory_game_completed:
                    print('Menu: le joueur a cliqué sur le jeu "mémo"')
                    sound_click.play()
                    state = MEMORY_STATE
                elif TICTACTOE_BUTTON_RECT.collidepoint(event.pos) and not tictactoe_game_completed:
                    print('Menu: le joueur a cliqué sur le jeu "morpion"')
                    sound_click.play()
                    state = TIC_TAC_TOE_STATE
                elif QUIZ_BUTTON_RECT.collidepoint(event.pos) and not quiz_game_completed:
                    print('Menu: le joueur a cliqué sur le jeu "quiz"')
                    sound_click.play()
                    state = QUIZ_STATE

            else:
                # Gestion du bouton de retour au menu de la score-barre
                menu_button_text_font = pygame.font.Font(GAME_FONTS, 24)
                menu_button_text_surface = menu_button_text_font.render(SCORE_BARRE_MENU_BUTTON_TEXT, True, pygame.Color('gray44'))
                menu_button_text_rect = menu_button_text_surface.get_rect(topright=(fenetre_surface.get_width() - SCORE_BARRE_MENU_BUTTON_SIZE, SCORE_BARRE_MENU_BUTTON_MARGIN))
                if menu_button_text_rect.collidepoint(event.pos):
                    sound_click.play()
                    state = MENU_STATE

                if state == MEMORY_STATE:
                    if not memory_game_click_count >= MEMORY_GAME_MAX_TENTATIVES or not len(memory_game_cases_found) == len(memory_game_cases):
                        # On teste chaque case du mémo qui n'est ni déja sélectionnée ni déjà trouvée
                        cases = [case for case in memory_game_cases if case not in memory_game_cases_found and case not in memory_game_cases_selected]
                        for rect_info in cases:
                            if playerDelayDisplayUpdate == 0 and len(memory_game_cases_selected) <= 2 and rect_info['rectangle'].collidepoint(event.pos):
                                memory_game_cases_selected.append(rect_info)

                                # On teste si une paire de carte a été retournée
                                if len(memory_game_cases_selected) == 2:
                                    # on incrémente le nombre de tentatives
                                    memory_game_click_count += 1

                                    # Si la paire est incorrecte, on doit à nouveau cacher les cartes
                                    if memory_game_cases_selected[0]['image_index'] != memory_game_cases_selected[1]['image_index']:
                                        # On initialise un delai pour laisser au joueur le temps de voir la carte
                                        print(f'Mémo: tentative #{memory_game_click_count}: paire KO')
                                        sound_wrong.play()
                                        playerDelayDisplayUpdate = pygame.time.get_ticks() + 1000
                                    else:
                                        # On ajoute la paire aux cartes validées
                                        print(f'Mémo: tentative #{memory_game_click_count}: paire OK')
                                        sound_correct.play()
                                        memory_game_cases_found.extend(memory_game_cases_selected)
                                        memory_game_cases_selected.clear()
                                else:
                                    sound_click.play()

                elif state == TIC_TAC_TOE_STATE:
                    # On teste chaque case du tictactoe
                    for square_info in tictactoe_game_cases:
                        if square_info['square'].collidepoint(event.pos):
                            # Si ce n'est pas une case déjà cliquées
                            if not square_info['clicked'] and tictactoe_game_player_turn:
                                sound_click.play()
                                square_info['clicked'] = 'player'
                                tictactoe_game_player_turn = False
                                playerDelayDisplayUpdate = pygame.time.get_ticks() + 1000

                elif state == QUIZ_STATE:
                    if playerDelayDisplayUpdate == 0 and quiz_game_current_question != None and lives > 0:
                        for item in quiz_game_current_question['answers']:
                            if item['rect'].collidepoint(event.pos):
                                # quand le joueur a choisi une réponse on déclenche le compteur
                                # pour laisser le temps de voir le résultat avant de passer à la question suivante
                                playerDelayDisplayUpdate = pygame.time.get_ticks() + 2000

                                # si c'est la bonne réponse, on incrémente le score
                                if item['isCorrect']:
                                    sound_correct.play()
                                    quiz_game_score += 1
                                else:
                                    sound_wrong.play()

    # On affiche les différents écran du jeux en fonction de l'état de "state"
    if state == START_STATE:
        display_start_screen(game_scenario)

    if state == LEVEL_STATE:
        display_level_screen()

    elif state == MENU_STATE:
        if lives == 0 or (quiz_game_completed and tictactoe_game_completed and memory_game_completed):
            # quand le joueur a complété les 3 jeux ou épuisé toutes les vies
            # pour lui laisser le temps de voir le résultat on met un délai
            if gameoverDelayDisplayUpdate == 0:
                gameoverDelayDisplayUpdate = pygame.time.get_ticks() + 2000
            if gameoverDelayDisplayUpdate > 0 and pygame.time.get_ticks() >= gameoverDelayDisplayUpdate:
                state = END_STATE

        display_menu_screen()
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
            playerDelayDisplayUpdate = 0

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
                                    {"text": "Gagné !", "color": pygame.Color('green')})

            # Au delà de 10 tentatives on perd une vie
            elif memory_game_click_count >= MEMORY_GAME_MAX_TENTATIVES:
                display_score_barre(lives, True,
                                    f"Nombre de tentatives: {memory_game_click_count}",
                                    {"text": "Perdu !", "color": pygame.Color('red')})

            if pygame.time.get_ticks() >= gameoverDelayDisplayUpdate:

                if len(memory_game_cases_found) < len(memory_game_cases):
                    sound_lost.play()
                    # On décrémente le nombre de vies
                    if lives > 0:
                        lives -= 1
                        memory_game_cases_found.clear()
                        memory_game_cases_selected.clear()
                        # S'il reste au moins 1 vie au joueur on réinitialise le mémo
                        if lives >= 1:
                            memory_game_cases.clear()
                else:
                    memory_game_completed = True
                    sound_win.play()

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

        # On regarde si la partie est terminée
        winner = check_tictactoe_game_over(tictactoe_game_cases)
        if winner != None:
            # On ajoute un délai (2s) en fin de partie pour avoir le temps de voir le résultat
            if gameoverDelayDisplayUpdate == 0:
                print(f"Tic Tac Toe: le gagnant est {winner}")
                gameoverDelayDisplayUpdate = pygame.time.get_ticks() + 2000

            if 'player' in winner:
                display_score_barre(lives, True, "fin de la partie: ", {"text": "Gagné !", "color": pygame.Color('green')})
            elif 'computer' in winner:
                display_score_barre(lives, True, "fin de la partie: ", {"text": "Perdu !", "color": pygame.Color('red')})
            else:
                display_score_barre(lives, True, "fin de la partie: ", {"text": "Egalité !", "color": pygame.Color('blue')})

            if pygame.time.get_ticks() >= gameoverDelayDisplayUpdate:
                # On décrémente le nombre de vies si le joueur a perdu
                if 'computer' in winner:
                    sound_lost.play()
                    # On décrémente le nombre de vies
                    if lives > 0:
                        lives -= 1
                        # S'il reste au moins 1 vie au joueur on réinitialise le mémo
                        if lives >= 1:
                            tictactoe_game_cases.clear()
                # En cas d'égalité le joueur peut rejouer sans perdre de vie
                elif 'égalité' in winner:
                    sound_lost.play()
                    # On réinitialise le mémo
                    tictactoe_game_cases.clear()
                else:
                    tictactoe_game_completed = True
                    sound_win.play()

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
        # Initilise le quiz s'il ne l'est pas déjà
        if not quiz_game_current_question and quiz_game_questions == [] and lives > 0:
            playerDelayDisplayUpdate = 0
            gameoverDelayDisplayUpdate = 0
            quiz_game_questions = initialize_quiz_game()

        if len(quiz_game_questions) > 0:
            # on regarde si on a une nouvelle à afficher
            if not quiz_game_current_question or \
               (playerDelayDisplayUpdate > 0 and pygame.time.get_ticks() >= playerDelayDisplayUpdate):
                quiz_game_current_question = quiz_game_questions.pop()
                playerDelayDisplayUpdate = 0

            display_score_barre(lives, True, f"{str(quiz_game_score)}/{str(QUIZ_GAME_WIN_LIMIT)} bonnes réponses attendues")

        elif playerDelayDisplayUpdate > 0 and pygame.time.get_ticks() >= playerDelayDisplayUpdate:
            # On ajoute un délai (2s) en fin de partie pour avoir le temps de voir le résultat
            if gameoverDelayDisplayUpdate == 0:
                print(f"Quiz: partie terminée avec le score {str(quiz_game_score)}/{str(QUIZ_GAME_MAX_QUESTIONS)}")
                gameoverDelayDisplayUpdate = pygame.time.get_ticks() + 2000

            # on a affiché toutes questions, il faut vérifier si le joueur a gagné ou perdu
            if quiz_game_score >= QUIZ_GAME_WIN_LIMIT:
                display_score_barre(lives, True,
                                    f"Bonnes réponses: {str(quiz_game_score)}",
                                    {"text": "Gagné !", "color": pygame.Color('green')})
            else:
                display_score_barre(lives, True,
                                    f"Bonnes réponses: {str(quiz_game_score)}/8 nécessaires",
                                    {"text": "Perdu !", "color": pygame.Color('red')})

            if pygame.time.get_ticks() >= gameoverDelayDisplayUpdate:
                if quiz_game_score < QUIZ_GAME_WIN_LIMIT:
                    sound_lost.play()
                    # On décrémente le nombre de vies
                    if lives > 0 and quiz_game_score < QUIZ_GAME_WIN_LIMIT:
                        lives -= 1
                        # S'il reste au moins 1 vie au joueur on réinitialise le quiz
                        if lives >= 1:
                            quiz_game_current_question = None
                else:
                    quiz_game_completed = True
                    sound_win.play()

                quiz_game_score = 0
                gameoverDelayDisplayUpdate = 0
                # On retourne au menu
                state = MENU_STATE

        if quiz_game_current_question != None:
            display_quiz_game(quiz_game_current_question)

    elif state == END_STATE:
        # Si le nombre de vie est supérieur à 0 c'est que le joueur a gagné
        if lives > 0:
            # On utilise ce booléen pour ne jouer le son qu'une seule fois
            if not game_over:
                game_over = True
                sound_win.play()

            display_final_screen(game_scenario['conclusionWin'])

        # Sinon il a perdu
        else:
            if not game_over:
                game_over = True
                sound_lost.play()

            display_final_screen(game_scenario['conclusionLose'])

    display_cursor()

    pygame.display.update()
    clock.tick(60)