import pygame
import sys
import variables, outils

MEMO_BUTTON_RECT = pygame.Rect(0, 50, 193, 256)
TICTACTOE_BUTTON_RECT = pygame.Rect(0, 311, 193, 289)
QUIZ_BUTTON_RECT = pygame.Rect(365, 250, 235, 350)

def afficher_bouton(image, rect, text="", color="black"):
    fenetre_surface = pygame.display.get_surface()

    # Charger l'image du bouton
    button_image = pygame.image.load(image).convert()

    # Dessiner le rectangle du bouton
    pygame.draw.rect(fenetre_surface, pygame.Color('white'), rect, 2)

    # Mettre à l'échelle l'image pour qu'elle s'adapte à la taille du bouton
    button_image = pygame.transform.scale(button_image, rect.size)

    # Ajouter du texte au bouton
    if text != "":
        text_font = pygame.font.Font(variables.GAME_FONTS, 24)
        text_surface = text_font.render(text, True, pygame.Color(color))
        text_rect = text_surface.get_rect(center=button_image.get_rect().center)
        button_image.blit(text_surface, text_rect.topleft)

    # Blitter le bouton sur l'écran
    fenetre_surface.blit(button_image, rect)

def screen():
    # Play the quiz game
    fenetre_surface = pygame.display.get_surface()
    
    # Fond d'écran
    menu_background = outils.image_surface(variables.MENU_BACKGROUND_IMAGE, fenetre_surface.get_width(), fenetre_surface.get_height())
    fenetre_surface.blit(menu_background, (0, 0))

    afficher_bouton(variables.MEMORY_BACKGROUND_IMAGE, MEMO_BUTTON_RECT, text="Mémo")
    afficher_bouton(variables.TICTACTOE_BACKGROUND_IMAGE, TICTACTOE_BUTTON_RECT, text="Morpion")
    afficher_bouton(variables.QUIZ_BACKGROUND_IMAGE, QUIZ_BUTTON_RECT, text="Quiz")

    # Affiche la barre de score
    outils.score_barre()    


def events(mousePosition):
    outils.score_barre_events(mousePosition)

    fenetre_surface = pygame.display.get_surface()
    if MEMO_BUTTON_RECT.collidepoint(mousePosition):
       pygame.draw.rect(fenetre_surface, pygame.Color('lightblue'), MEMO_BUTTON_RECT, 2)
       variables.state = variables.MEMORY_STATE
    elif TICTACTOE_BUTTON_RECT.collidepoint(mousePosition):
        pygame.draw.rect(fenetre_surface, pygame.Color('lightblue'), TICTACTOE_BUTTON_RECT, 2)
        variables.state = variables.TIC_TAC_TOE_STATE
    elif QUIZ_BUTTON_RECT.collidepoint(mousePosition):
        pygame.draw.rect(fenetre_surface, pygame.Color('lightblue'), QUIZ_BUTTON_RECT, 2)
        variables.state = variables.QUIZ_STATE


if __name__ == "__main__":
    # Initialise PyGame
    pygame.init()
    pygame.display.set_caption("Quiz")
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