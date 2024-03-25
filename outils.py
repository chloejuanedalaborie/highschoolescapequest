import pygame
import variables

MENU_BUTTON_SIZE = 50
MENU_BUTTON_MARGIN = 10
MENU_BUTTON_TEXT = "Menu"

def image_surface(fichier, width, height, transparent=False):
    if transparent:
        surface = pygame.image.load(fichier).convert_alpha()
    else:
        surface = pygame.image.load(fichier).convert()
    surface = pygame.transform.scale(surface, (width, height))
    return surface

def afficher_curseur():
    pygame.mouse.set_visible(False) # cache le pointeur par défaut
    fenetre_surface = pygame.display.get_surface()
    cursor_surface = image_surface("./images/curseur.png", 50, 50, True)

    coord = cursor_surface.get_rect()
    coord.center = pygame.mouse.get_pos()
    fenetre_surface.blit(cursor_surface, coord)

def text_button_definition(text):
    menu_font = pygame.font.Font(variables.GAME_FONTS, 24)
    surface = menu_font.render(text, True, pygame.Color('gray44'))
    fenetre_surface = pygame.display.get_surface()
    rect = surface.get_rect(topright=(fenetre_surface.get_width() - MENU_BUTTON_SIZE, MENU_BUTTON_MARGIN))

    return surface, rect

# Function to draw the menu button
def menu_button():
    button_text_surface, button_text_rect = text_button_definition(MENU_BUTTON_TEXT)
    fenetre_surface = pygame.display.get_surface()
    fenetre_surface.blit(button_text_surface, button_text_rect)

    if button_text_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(fenetre_surface, pygame.Color('lightblue'), button_text_rect, 2)  

def score_barre(bShowMenuButton=False, sScoreText="", dGameOverText={}):
    life_full_image = image_surface("./images/Icon_Large_HeartFull.png", 15, 15, True)
    life_empty_image = image_surface("./images/Icon_Large_HeartEmpty.png", 15, 15, True)

    # Affiche la barre de score
    fenetre_surface = pygame.display.get_surface()
    score_barre_rect = pygame.Rect(0, 0, fenetre_surface.get_width(), variables.SCORE_BARRE_HEIGHT)
    pygame.draw.rect(fenetre_surface, pygame.Color('white'), score_barre_rect, 0)

    # Vie: <livesCount>                                         |  Menu   |
    # <score_text>         < gameover_text >                    |  Button |

    score_text_font = pygame.font.Font(variables.GAME_FONTS, 12)
    gameover_font = pygame.font.Font(variables.GAME_FONTS, 48)

    # Affichage du nombre de vies
    life_text_surface = score_text_font.render("Vies :", True, pygame.Color('gray44'))
    life_text_rect = life_text_surface.get_rect(topleft=(10, 10))
    fenetre_surface.blit(life_text_surface, life_text_rect)
    for life_full in range(variables.livesCount):
        fenetre_surface.blit(life_full_image, (life_text_rect.width + 20 + (life_full * life_full_image.get_width()), 10))
    for life_empty in range(variables.MAX_LIVES - variables.livesCount):
        fenetre_surface.blit(life_empty_image, (life_text_rect.width + 20 + (variables.livesCount * (life_full_image.get_width())) + (life_empty * life_empty_image.get_width()), 10))

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
        # Affiche le bouton menu
        menu_button()

def menu_button_events(mousePosition):
    button_text_surface, button_text_rect = text_button_definition(MENU_BUTTON_TEXT)
    # Gestion du bouton de retour au menu
    if button_text_rect.collidepoint(mousePosition):
        variables.state = variables.MENU_STATE

def score_barre_events(mousePosition):
    menu_button_events(mousePosition)