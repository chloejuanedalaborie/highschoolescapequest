import pygame
import sys
import variables, outils

def screen():
    # Play the quiz game
    fenetre_surface = pygame.display.get_surface()
    
    # Fond d'écran
    quiz_background = outils.image_surface("./images/salle_quiz.png", fenetre_surface.get_width(), fenetre_surface.get_height() - variables.SCORE_BARRE_HEIGHT)
    fenetre_surface.blit(quiz_background, (0, variables.SCORE_BARRE_HEIGHT))

    # Affiche la barre de score
    outils.score_barre(True)    

def events(mousePosition):
    outils.score_barre_events(mousePosition)

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